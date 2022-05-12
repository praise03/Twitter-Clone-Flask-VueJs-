from functools import wraps
from flask import request, jsonify
from models import User


def token_required(f):
    @wraps(f)
    def require_token(*args, **kwargs):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            if token.startswith('Bearer '):
                token = token[7:]
        else:
            return jsonify({
                'message': 'Request does not contain an authorization token'
            })

        try:
            valid = True if User.decode_token(token) == 1 else False

            if valid:
                print('Auth Successful')
            elif User.decode_token(token) == 'Token Expired':
                return jsonify({'message': 'Token Expired'})
            else:
                return jsonify({
                    'message': 'Invalid token supplied'
                })
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "error": str(e)
            })
        return f(*args, **kwargs)
    return require_token
