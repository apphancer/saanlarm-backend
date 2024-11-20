import jwt
import datetime
from functools import wraps
from flask import request, jsonify
import config_local as config
from werkzeug.security import generate_password_hash, check_password_hash

SECRET_KEY = config.SECRET_KEY

USERS = {
    config.USER: generate_password_hash(config.PASSWORD)
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-tokens')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode({
        'user': username,
        'exp': expiration_time
    }, SECRET_KEY, algorithm="HS256")
    return token, expiration_time