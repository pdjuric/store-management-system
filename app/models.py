from operator import and_

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)


class ProductOrder(db.Model):
    __tablename__ = 'product_order'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    received = db.Column(db.Integer, nullable=False)
    requested = db.Column(db.Integer, nullable=False)
    buying_price = db.Column(db.Float, nullable=False)

    # order = db.relationship('Order', uselist=False)

    @staticmethod
    def get_incomplete(product_id):
        return ProductOrder.query.filter(and_(ProductOrder.received < ProductOrder.requested, ProductOrder.product_id == product_id))\
            .join(Order, Order.id == ProductOrder.order_id).order_by(Order.timestamp.asc()).all()

    def get_missing(self):
        return self.requested - self.received

    @staticmethod
    def json_all_products_for_order(order_id):
        products = db.session.query(ProductOrder, Product)\
            .select_from(ProductOrder).join(Product, Product.id == ProductOrder.product_id).filter(ProductOrder.order_id == order_id).all()

        return [{
            'categories': [str(c) for c in p.categories],
            'name': p.name,
            'price': p_o.buying_price,
            'requested': p_o.requested,
            'received': p_o.received
        } for p_o, p in products]


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    waiting = db.Column(db.Integer, nullable=False, default=0)

    categories = db.relationship('Category', secondary=ProductCategory.__table__, back_populates='products')
    orders = db.relationship('Order', secondary=ProductOrder.__table__, back_populates='products')

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'categories': [str(c) for c in self.categories]
        }


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    products = db.relationship('Product', secondary=ProductCategory.__table__, back_populates='categories')

    def __repr__(self):
        return self.name


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(8), nullable=False, default='COMPLETE')
    timestamp = db.Column(db.DateTime, nullable=False)

    products = db.relationship('Product', secondary=ProductOrder.__table__, back_populates='orders')
    # order_items = db.relationship('Product_Order')

    def setPending(self):
        self.status = 'PENDING'
        db.session.add(self)  # TODO: da li ovo radi?

    def check_completed(self):

        #  TODO: ako radi relacija

        if ProductOrder.query.filter(and_(
            ProductOrder.received < ProductOrder.requested,
            ProductOrder.order_id == self.id
        )).count() == 0:
            self.status = 'COMPLETE'
            db.session.add(self)


    @property
    def json(self):
        return {
            'products': ProductOrder.json_all_products_for_order(order_id=self.id),
            'price': self.price,
            'status': self.status,
            'timestamp': self.timestamp
        }