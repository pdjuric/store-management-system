import sqlalchemy
from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt_identity, get_jwt
import re
from sqlalchemy import and_
from common.roleCheck import role
from configuration import Configuration
from models import db, User, Role

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
jwt = JWTManager(app)


def check_email(email):
    email = email.lower()
    regex = "([a-z0-9]+[.-_])*[a-z0-9]+@[a-z0-9-]+(\.[a-z]{2,})+"
    return re.fullmatch(regex, email) is not None


def check_password(password):
    has_length = len(password) >= 8
    has_digit = re.search("\d", password) is not None
    has_lower = re.search("[a-z]", password) is not None
    has_upper = re.search("[A-Z]", password) is not None
    return has_length and has_digit and has_lower and has_upper


@app.route('/register', methods=['POST'])
def register():
    form_data = {}

    for t in ['forename', 'surname', 'email', 'password', 'isCustomer']:
        form_data[t] = request.json.get(t, None)
        if form_data[t] is None or t != 'isCustomer' and len(form_data[t]) == 0:
            return jsonify(message=f'Field {t} is missing.'), 400

    if form_data['email'] is not None and not check_email(form_data['email']):
        return jsonify(message='Invalid email.'), 400

    if form_data['password'] is not None and not check_password(form_data['password']):
        return jsonify(message='Invalid password.'), 400

    role = Role.query.filter(Role.id == ('customer' if form_data['isCustomer'] else 'worker')).first()
    user = User(email=form_data['email'].lower(), password=form_data['password'], forename=form_data['forename'], surname=form_data['surname'], role=role)
    db.session.add(user)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return jsonify(message='Email already exists.'), 400

    return Response(status=200)


@app.route('/login', methods=['POST'])
def login():
    form_data = {}

    for t in ['email', 'password']:
        form_data[t] = request.json.get(t, None)
        if form_data[t] is None or len(form_data[t]) == 0:
            return jsonify(message=f'Field {t} is missing.'), 400

    if form_data['email'] is not None and not check_email(form_data['email']):
        return jsonify(message='Invalid email.'), 400

    user = User.query.filter(and_(
        User.email == form_data['email'].lower(),
        User.password == form_data['password'])).first()
    if not user:
        return jsonify(message='Invalid credentials.'), 400

    additional_claims = {
        'forename': user.forename,
        'surname': user.surname,
        'email': user.email,
        'password': user.password,
        'isCustomer': user.role == 'customer',
        'role': user.role
    }

    access_token = create_access_token(identity=user.email, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.email, additional_claims=additional_claims)

    return jsonify(accessToken=access_token, refreshToken=refresh_token)


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    additional_claims = get_jwt()
    return Response(create_access_token(identity=identity, additional_claims=additional_claims), status=200)


@app.route('/delete', methods=['POST'])
@role('admin')
def delete():
    logged_user = User.query.filter(User.email == get_jwt_identity()).first()
    if logged_user.role != 'admin':
        return jsonify(message='Access denied.'), 403

    form_data = {'email': request.json.get('email', None)}

    if form_data['email'] is None or len(form_data['email']) == 0:
        return jsonify(message='Field email is missing.'), 400

    if form_data['email'] is not None and not check_email(form_data['email']):
        return jsonify(message='Invalid email.'), 400

    user = User.query.filter(User.email == form_data['email']).first()
    if not user:
        return jsonify(message='Unknown user.'), 400
    else:
        User.query.filter(User.email == form_data['email']).delete()
        db.session.commit()
        return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
