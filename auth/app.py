import sqlalchemy
from flask import Flask, request, Response, jsonify
from flask_migrate import Migrate
import re
from configuration import Configuration
from models import db, User
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
migrateObj = Migrate(app, db)


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
    message = ""
    form_data = {}

    for t in ['forename', 'surname', 'email', 'password', 'isCustomer']:
        if request.json.get(t) is None or t != 'isCustomer' and len(request.json.get(t)) == 0:
            message += f'Field {t} is missing. '
        else:
            form_data[t] = request.json.get(t)

    if not check_email(form_data['email']):
        message += 'Invalid email. '

    if not check_password(form_data['password']):
        message += 'Invalid password. '

    if len(message) == 0:
        user = User(email=form_data['email'], password=form_data['password'], forename=form_data['forename'], surname=form_data['surname'])
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            message += 'Email already exists.'

    if len(message) == 0:
        return Response(status=200)
    else:
        return jsonify(message=message), 400


@app.route('/init', methods=['GET'])
def initialise():
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    with app.app_context() as context:
        init()
        migrate()
        upgrade()
        #
        # adminRole = Role(name='admin')
        # userRole = Role(name='user')
        #
        # database.session.add(adminRole)
        # database.session.add(userRole)
        # database.session.commit()
        #
        # admin = User(email='admin@admin.com', password='1', forename='admin', surname='admin')
        # database.session.add(admin)
        # database.session.commit()
        #
        # userRole = UserRole(userId=admin.id, roleId=adminRole.id)






if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
