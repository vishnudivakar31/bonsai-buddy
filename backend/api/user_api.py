from flask import Blueprint, request, jsonify, make_response
from models.user import User
from database import db

user_api = Blueprint('user_api', __name__)

@user_api.route("/user/register", methods=['POST'])
def register():
    payload = request.get_json()
    user = User(payload['username'], payload['email'], password=payload['password'])
    try:
        db.session.add(user)
        db.session.commit()
        response = make_response(jsonify(user.to_dict()), 201)
    except Exception as e:
        response = make_response(jsonify({"cause": str(e)}), 500)
    response.headers["Content-Type"] = "application/json"
    return response
