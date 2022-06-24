from flask import request, jsonify, Response, Flask
import csv
import io

from flask_jwt_extended import JWTManager
from redis import Redis
from configuration import Configuration
from common.roleCheck import role

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route('/update', methods=['POST'])
@role('worker')
def addProducts():
    if 'file' not in request.files.keys():
        return jsonify(message='Field file is missing.'), 400
    content = request.files['file'].stream.read().decode('utf-8')
    stream = io.StringIO(content)
    reader = csv.reader(stream)

    rows = []
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
            product_price = float(row[3])
            if product_price <= 0:
                raise ValueError
        except ValueError:
            return jsonify(message=f'Incorrect price on line {line}.'), 400

        rows.append(row)
        line += 1

    with Redis(host=Configuration.REDIS_HOST) as redis:
        for row in rows:
            redis.rpush(Configuration.REDIS_LIST, ','.join(row))

    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)