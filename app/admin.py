from flask import jsonify, Flask
from flask_jwt_extended import JWTManager
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce
from models import Product, db, ProductOrder, Category, ProductCategory
from configuration import Configuration
from common.roleCheck import role

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
jwt = JWTManager(app)


@app.route('/productStatistics', methods=['GET'])
@role('admin')
def product_statistics():
    products = db.session \
        .query(Product.name,
               func.sum(ProductOrder.requested) - func.sum(ProductOrder.received),
               func.sum(ProductOrder.requested)) \
        .join(Product, Product.id == ProductOrder.product_id) \
        .group_by(ProductOrder.product_id) \
        .all()

    return jsonify(statistics=[{
        "name": p[0],
        "waiting": int(p[1]),
        "sold": int(p[2])
    } for p in products])


@app.route('/categoryStatistics', methods=['GET'])
@role('admin')
def category_statistics():
    categories = db.session\
        .query(Category.name) \
        .select_from(Category) \
        .join(ProductCategory, ProductCategory.category_id == Category.id) \
        .outerjoin(ProductOrder, ProductOrder.product_id == ProductCategory.product_id) \
        .group_by(Category.name) \
        .order_by(func.sum(coalesce(ProductOrder.requested, 0)).desc(), Category.name.asc()) \
        .all()

    return jsonify(statistics=[c.name for c in categories])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
