from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    sold = db.Column(db.Integer, nullable=False, default=0)
    waiting = db.Column(db.Integer, nullable=False, default=0)


    categories = db.relationship('Category', secondary=ProductCategory.__table__, back_populates='products')
    orders = db.relationship('Ordeer', secondary=ProductCategory.__table__, back_populates='products')

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'categories': [str(c) for c in self.categories]
        }


class ProductOrder(db.Model):
    __tablename__ = 'product_order'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    received = db.Column(db.Integer, nullable=False)
    requested = db.Column(db.Integer, nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    products = db.relationship('Product', secondary=ProductCategory.__table__, back_populates='categories')
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return self.name


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(8), nullable=False, default='PENDING')
    timestamp = db.Column(db.DateTime, nullable=False)

    products = db.relationship('Product', secondary=ProductOrder.__table__, back_populates='orders')
