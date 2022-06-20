from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    forename = db.Column(db.String(256), nullable=False)
    surname = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(256), db.ForeignKey('roles.id'), nullable=False)
    # isCustomer = db.Column(db.Boolean, default=False)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.String(256), primary_key=True)
    users = db.relationship('User')

    def __repr__(self):
        return self.id
