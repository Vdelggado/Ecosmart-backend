from flask import Blueprint,jsonify, request
from ..models.auth import select_user_by_email, insert_user, get_user_by_id
from ..utils.validator import validateRegister, validateLogin
from ..utils.hash import hash_password , check_password
from src.utils.jwt import create_jwt_token
from flask_jwt_extended import get_jwt_identity, jwt_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    isValid = validateLogin(email, password)
    
    if not isValid[0]:  
        return jsonify({"ok":False,'message': isValid[1]}), 400

    user = select_user_by_email(email)
    
    if user["success"] == False:
        return jsonify({ "ok":False,'message': user["message"] }), 500
    
    if not user["user"]  or not check_password(password, user["user"].get('password')):
        return jsonify({"ok":False,'message': 'User or password incorrect'}), 401
    
    
    jwt_token = create_jwt_token(user["user"].get('user_id'), user["user"].get('name'))
    
    return jsonify({"ok":True,'access_token': jwt_token}), 200


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    lastname = data.get('lastname')
    
    isValid = validateRegister(name, password, email,lastname)
    
    if not isValid[0]:
        return jsonify({"ok":False,'message': isValid[1]}), 400
    
    exists = select_user_by_email(email)
    
    if exists["user"]:
        return jsonify({"ok":False,'message': 'Email already exists'}), 400
    
    if exists["success"] == False:
        return jsonify({"ok":False,'message': exists["message"]}), 500
    
    hashed_password = hash_password(password)   
    
    created = insert_user(name, lastname, email, hashed_password)
    
    if not created:
         return jsonify({"ok":False,'message': 'User not created'}), 500
     
    return jsonify({"ok":True,'message': 'User created'}), 201
    

@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user = get_jwt_identity()
    user_data = get_user_by_id(user.get('id'))
    
    if not user_data["success"]:
        return jsonify({"ok":False,'message': user_data["message"]}), 500
    
    if not user_data["user"]:
        return jsonify({"ok":False,'message': 'User not found'}), 404
    user = user_data["user"]
    
    return jsonify({"ok":True,'user': user}), 200
 