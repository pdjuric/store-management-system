import csv
import io
from flask import Flask
from redis import Redis
from models import Product, Category, db, ProductOrder, Order
from configuration import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)

while True:
    with Redis(host=Configuration.REDIS_HOST) as redis:
        message = redis.blpop(Configuration.REDIS_LIST)
        stream = io.StringIO(message[1].decode('utf-8'))
        reader = csv.reader(stream)
        for row in reader:
            categories, product_name, product_quantity, product_price = row[0].split('|'), row[1], int(row[2]), float(row[3])

        with app.app_context() as context:
            product = Product.query.filter(Product.name == product_name).first()

            if not product:
                category_arr = []
                for name in categories:
                    category = Category.query.filter(Category.name == name).first()
                    if not category:
                        category = Category(name=name)
                        db.session.add(category)
                    category_arr.append(category)
                db.session.commit()

                product = Product(name=product_name, quantity=product_quantity, price=product_price, categories=category_arr)
                db.session.add(product)
                db.session.commit()

            elif len(product.categories) == len(categories) and [c.name for c in product.categories if c.name not in categories] == []:

                product.price = (product.quantity * product.price + product_quantity * product_price) / (product.quantity + product_quantity)
                product.quantity += product_quantity
                db.session.add(product)

                for order_item in ProductOrder.get_incomplete(product.id):
                    received = min(product.quantity, order_item.get_missing())
                    if received > 0:
                        product.waiting -= received
                        product.quantity -= received
                        order_item.received += received

                        if order_item.requested == order_item.received:
                            Order.get(order_item.order_id).check_completed()

                        db.session.add( order_item)
                    else:
                        break

                db.session.commit()
