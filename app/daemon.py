import csv
import io
from redis import Redis
from models import Product, Category, ProductCategory, db
from configuration import Configuration

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

            if len(product.categories) != len(categories):
                break #???
            for c in categories:
                if c not in product.categories:
                    break #???

            product.price = (product.quantity * product.price + product_quantity * product_price) / (product.quantity + product_quantity)
            product.quantity += product_quantity

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

        #proveri da li neko ceka na ovo !!
