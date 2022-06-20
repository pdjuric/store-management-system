from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database
from configuration import Configuration
from models import db, Role, User

app = Flask(__name__)
app.config.from_object(Configuration)

migrate_ = Migrate(app, db)

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

db.init_app(app)

with app.app_context() as context:
    init()
    migrate()
    upgrade()

    admin_role = Role(id='admin')
    worker_role = Role(id='worker')
    customer_role = Role(id='customer')

    db.session.add(admin_role)
    db.session.add(worker_role)
    db.session.add(customer_role)
    db.session.commit()

    admin = User(email='admin@admin.com', password='1', forename='admin', surname='admin', role=admin_role)
    db.session.add(admin)
    db.session.commit()
