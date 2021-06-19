from flask import Blueprint, request, jsonify, make_response
import os
import uuid
from models.product import Product
from models.user import User, UserType
from database import db
from PIL import Image

product_api = Blueprint('product_api', __name__)

BASE_FILE_PATH = '../files'

def create_directory(directory_name):
    path = '{}/{}'.format(BASE_FILE_PATH, directory_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def save_image(path_name, image):
    return image.save(path_name)

@product_api.route('/product')
def index():
    userID = int(request.args.get('userID'))
    user = User.query.get(userID)
    if user is not None:
        products = Product.query.all()
        if user.user_type == UserType.USER:
            products = filter(lambda x: x.verified == True, products)
        response = make_response(jsonify([x.to_dict() for x in products]), 200)
    else:
        response = make_response(jsonify({"cause": "user not found"}), 500)
    response.headers["Content-Type"] = "application/json"
    return response
    
@product_api.route("/product/register", methods=['POST'])
def register():
    payload = request.get_json()
    product = Product(payload['name'], '')
    try:
        db.session.add(product)
        db.session.commit()
        response = make_response(jsonify(product.to_dict()), 201)
    except Exception as e:
        response = make_response(jsonify({"cause": str(e)}), 500)
    response.headers["Content-Type"] = "application/json"
    return response

@product_api.route("/product/verify", methods=['GET'])
def verify():
    userID = int(request.args.get('userID'))
    productID = int(request.args.get('productID'))
    verify_status = (request.args.get('verify_status').lower() == 'true')
    user = User.query.get(userID)
    if user is not None:
        if user.user_type == UserType.ADMIN:
            product = Product.query.get(productID)
            if product is not None and verify_status == True:
                product.verified = True
                product.file_path = create_directory(product.name)
                db.session.commit()
                response = make_response(jsonify(product.to_dict()), 200)
            elif product is not None and verify_status == False:
                db.session.delete(product)
                db.session.commit()
                response = make_response(jsonify(product.to_dict()), 200)
            else:
                response = make_response(jsonify({'cause': 'product not found'}), 500)
        else:
            response = make_response(jsonify({'cause': 'you are not admin.'}), 500)
    else:
        response = make_response(jsonify({'cause': 'user not found'}), 500)
    response.headers["Content-Type"] = "application/json"
    return response

@product_api.route('/product/image', methods=['POST'])
def upload_image():
    productID = int(request.args.get('productID'))
    userID = int(request.args.get('userID'))
    user = User.query.get(userID)
    if user is not None:
        product = Product.query.get(productID)
        if product.verified == True:
            path = '{}/{}/{}.png'.format(BASE_FILE_PATH, product.name, uuid.uuid4().hex)
            file = request.files['image']
            img = Image.open(file.stream)
            save_image(path, img)
            response = make_response(jsonify({'msg': 'success', 'size': [img.width, img.height]}), 200)
        else:
            response = make_response(jsonify({'cause': 'product not verified'}), 500)
    else:
        response = make_response(jsonify({'cause': 'user not found'}), 500)
    response.headers["Content-Type"] = "application/json"
    return response
