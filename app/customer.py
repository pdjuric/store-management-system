from flask import request, jsonify, Response, Flask
from sqlalchemy import or_, and_

from models import Product, Category, ProductCategory
from configuration import Configuration
from common.roleCheck import role

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/search', methods=['GET'])
@role('customer')
def searchProducts():
    product_name = request.get('name', default='')
    category_name = request.get('category', default='')

    products = Product.query.join(Product.categories).filter(and_(
        Product.name.like(f"%{product_name}%"),
        Category.name.like(f"%{category_name}%")
    )).all()

    categories = Category.query.join(Category.products).filter(and_(
        Product.name.like(f"%{product_name}%"),
        Category.name.like(f"%{category_name}%")
    )).all()

    return jsonify(categories=[str(c) for c in categories],
                   products=[p.json for p in products])



if __name__ == '__main__':
    app.run(debug=True)
