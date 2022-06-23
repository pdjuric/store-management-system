import csv
import io
from flask import Flask
from redis import Redis
from models import Product, Category, ProductCategory, db, ProductOrder
from configuration import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)

with app.app_context() as context:
    with Redis(host=Configuration.REDIS_HOST) as redis:
        while True:
            message = redis.blpop('new_product')
            stream = io.StringIO(message)
            reader = csv.reader(stream)
            for row in reader:
                categories, product_name, product_quantity, product_price = row[0].split('|'), row[1], int(row[2]), float(row[3])
                break

            product = Product.query.filter(Product.name == product_name).first()
            if product:

                # TODO: what to do when it breaks?
                if len(product.categories) != len(categories) or len([c for c in categories if c not in product.categories]) != 0:
                    break

                product.price = (product.quantity * product.price + product_quantity * product_price) / (product.quantity + product_quantity)
                product.quantity += product_quantity
                db.session.add(product)

                if product.waiting == 0:
                    break

                for item in ProductOrder.get_incomplete(product.id):
                    added = min(product_quantity, item.get_needed())
                    item.add(added)
                    product.sell(added)
                    product_quantity -= added

                db.commit()

            else:
                category_arr = []
                for name in categories:
                    category = Category.query.filter(Category.name == name).first()
                    if not category:
                        category = Category(name=name)
                        db.session.add(category)
                    category_arr.append(category)
                db.session.commit()

                product = Product(name=product_name, quantity=product_quantity, price=product_price, category=category_arr)
                db.session.add(product)
                db.session.commit()

                for c in category_arr:
                    db.session.add(ProductCategory(product_id=product.id, category_id=c.id))
                db.session.commit()
