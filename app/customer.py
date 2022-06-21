import datetime
from flask import request, jsonify, Response, Flask
from flask_jwt_extended import get_jwt
from sqlalchemy import and_

from models import Product, Category, db, Order, ProductOrder
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


@app.route('/order', methods=['POST'])
@role('customer')
def orderProducts():
    no = 0
    requests = request.json.get('requests')
    products = []
    quantities = []
    if not requests:
        return Response("Field requests is needed.", status=400)
    for item in requests:

        id_str = item.get('id')
        if not id_str:
            return Response(f"Product id is needed for request number {no}.", status=400)

        quantity_str = item.get('quantity')
        if not quantity_str:
            return Response(f"Product quantity is needed for request number {no}.", status=400)

        try:
            id = int(id_str)
            if id < 0: raise ValueError
        except ValueError:
            return Response(f"Invalid product id for request number {no}.", status=400)

        try:
            quantity = int(quantity_str)
            if quantity < 0: raise ValueError
        except ValueError:
            return Response(f"Invalid product quantity for request number {no}.", status=400)

        product = Product.query.get(id)
        if not product:
            return Response(f"Invalid product for request number {no}.", status=400)

        products.append(product)
        quantities.append(quantity)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    order = Order(user_id=get_jwt()['id'], timestamp=timestamp)
    db.session.add(order)
    db.session.commit()
    total_price = 0

    for product, requested in zip(products, quantities):
        success, received = product.try_to_sell(requested)
        if not success:
            order.setPending()

        total_price += product.price * requested
        product_order = ProductOrder(product_id=product.id, order_id=order.id, received=received, requested=requested, buying_price=product.price)
        db.session.add(product_order)
        db.session.commit()

    order.price = total_price
    db.session.add(order)
    db.session.commit()

    return jsonify(id=order.id), 200

if __name__ == '__main__':
    app.run(debug=True)
