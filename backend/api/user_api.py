from flask import Blueprint, request, jsonify, make_response
import hashlib, binascii, os
from models.user import User
from database import db

user_api = Blueprint('user_api', __name__)

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(hashed_password, password):
    salt = hashed_password[:64]
    stored_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

@user_api.route("/user/register", methods=['POST'])
def register():
    payload = request.get_json()
    user = User(payload['username'], payload['email'], password=hash_password(payload['password']), user_type=payload['user_type'])
    try:
        db.session.add(user)
        db.session.commit()
        response = make_response(jsonify(user.to_dict()), 201)
    except Exception as e:
        response = make_response(jsonify({"cause": str(e)}), 500)
    response.headers["Content-Type"] = "application/json"
    return response

@user_api.route("/user/login", methods=['POST'])
def login():
    payload = request.get_json()
    user = User.query.filter_by(username=payload['username']).first()
    if user is not None:
        if verify_password(user.password, payload['password']):
            response = make_response(jsonify(user.to_dict()), 200)
        else:
            response = make_response(jsonify({'cause': 'password or username is wrong'}), 401)
    else:
        response = make_response(jsonify({'cause': 'user account not found. create a new account'}), 401)
    response.headers["Content-Type"] = "application/json"
    return response
