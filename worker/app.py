from flask import request, jsonify, Response, Flask
import csv
import io
from redis import Redis
from configuration import Configuration
from common.roleCheck import role

app = Flask(__name__)
app.config.from_object(Configuration)

@app.route('/update', methods=['POST'])
@role('worker')
def addProducts():
    content = request.files['file'].stream.read().decode('utf-8')
    stream = io.StringIO(content)
    reader = csv.reader(stream)

    line = 0
    for row in reader:
        if len(row) != 4:
            return jsonify(message=f'Incorrect number of values on line {line}.'), 400
        # categories = row[0]
        # product_name = row[1]
        try:
            product_quantity = int(row[2])
            if product_quantity <= 0:
                raise ValueError
        except ValueError:
            return jsonify(message=f'Incorrect quantity on line {line}.'), 400

        try:
            product_price = int(row[3])
            if product_price <= 0:
                raise ValueError
        except ValueError:
            return jsonify(message=f'Incorrect price on line {line}.'), 400

        # TODO: slanje??

        with Redis(host=Configuration.REDIS_HOST) as redis:
            redis.publish('new_product', row)

        line += 1

    return Response(status=200)

