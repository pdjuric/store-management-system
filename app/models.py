from operator import and_

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
    orders = db.relationship('Order', secondary=ProductCategory.__table__, back_populates='products')

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'categories': [str(c) for c in self.categories]
        }

    def try_to_sell(self, needed):
        if self.sold < self.quantity and self.waiting == 0:
            available = min(self.quantity - self.sold, needed)
            self.sold += available
        else:
            available = 0

        if needed != available:
            self.waiting += needed - available

        db.session.add(self)

        return needed == available, available

    def sell(self, cnt):
        self.sold += cnt
        self.waiting -= cnt
        db.session.add(self)


class ProductOrder(db.Model):
    __tablename__ = 'product_order'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    received = db.Column(db.Integer, nullable=False)
    requested = db.Column(db.Integer, nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get_incomplete(product_id, product_id_match=True, order_id=None):
        conditions = [ProductOrder.received < ProductOrder.requested]
        if order_id is not None:
            conditions.append(ProductOrder.order_id == order_id)

        if product_id_match:
            conditions.append(ProductOrder.product_id == product_id)
        else:
            conditions.append(ProductOrder.product_id != product_id)

        return ProductOrder.query.filter(and_(*conditions)).order_by(ProductOrder.timestamp.asc()).all()

    def get_needed(self):
        return self.requested - self.received

    def add(self, cnt):
        self.requested += cnt
        if self.requested == self.received and len(ProductOrder(product_id=self.id, product_id_match=False, order_id=self.order_id)) == 0:
            Order.get(self.order_id).setComplete()
        db.session.add(self)


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
    price = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(8), nullable=False, default='COMPLETE')
    timestamp = db.Column(db.DateTime, nullable=False)

    products = db.relationship('Product', secondary=ProductOrder.__table__, back_populates='orders')

    def setComplete(self):
        self.status = 'COMPLETE'
        db.session.add(self)  # TODO: da li ovo radi?

    def setPending(self):
        self.status = 'PEENDING'
        db.session.add(self)  # TODO: da li ovo radi?

