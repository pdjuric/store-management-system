from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role(role):
    def innerRoleCheck(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if 'role' in claims and claims['role'] == role:
                return function(*args, **kwargs)
            else:
                return jsonify(msg='Missing Authorization Header'), 401

        return decorator
    return innerRoleCheck