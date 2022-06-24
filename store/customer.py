from flask import request, jsonify, Response, Flask
from flask_jwt_extended import get_jwt, JWTManager
from sqlalchemy import and_, func
from models import Product, Category, db, Order, ProductOrder
from configuration import Configuration
from common.roleCheck import role

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
jwt = JWTManager(app)


@app.route('/search', methods=['GET'])
@role('customer')
def searchProducts():
    product_name = request.args.get('name', default='')
    category_name = request.args.get('category', default='')

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
    products = []
    quantities = []
    if 'requests' not in request.json.keys():
        return jsonify(message='Field requests is missing.'), 400
    requests = request.json.get('requests')
    for item in requests:

        id_str = item.get('id')
        print(id_str)
        if not id_str:
            return jsonify(message=f'Product id is missing for request number {no}.'), 400

        quantity_str = item.get('quantity')
        print(quantity_str)
        if not quantity_str:
            return jsonify(message=f'Product quantity is missing for request number {no}.'), 400

        try:
            id = int(id_str)
            if id < 0: raise ValueError
        except ValueError:
            return jsonify(message=f'Invalid product id for request number {no}.'), 400

        try:
            quantity = int(quantity_str)
            if quantity < 0: raise ValueError
        except ValueError:
            return jsonify(message=f'Invalid product quantity for request number {no}.'), 400

        product = Product.query.get(id)
        if not product:
            return jsonify(message=f'Invalid product for request number {no}.'), 400

        products.append(product)
        quantities.append(quantity)
        no += 1

    timestamp = func.now()  # datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    order = Order(user_id=get_jwt()['id'], timestamp=timestamp)
    db.session.add(order)
    db.session.commit()
    total_price = 0

    for product, requested in zip(products, quantities):
        received = min(product.quantity, requested)
        if received > 0:
            product.quantity -= received
            db.session.add(product)

        if received != requested:
            order.setPending()

        total_price += product.price * requested
        product_order = ProductOrder(product_id=product.id, order_id=order.id, received=received, requested=requested, buying_price=product.price)
        db.session.add(product_order)

    order.price = total_price
    db.session.add(order)
    db.session.commit()

    return jsonify(id=order.id), 200


@app.route('/status', methods=['GET'])
@role('customer')
def orderStatus():
    orders = Order.query.filter(Order.user_id == get_jwt()['id']).all()
    return jsonify(orders=[o.json for o in orders])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
