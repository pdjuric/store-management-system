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

    caregories = db.relationship('Category', secondary=ProductCategory.__table__, back_populates='products')


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    products = db.relationship('Product', secondary=ProductCategory.__table__, back_populates='categories')
