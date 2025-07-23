from flask import Blueprint,jsonify, request
from src.utils.ecosmart import upload_image_to_cloudinary , process_order_items
from src.utils.validator import validateProduct, validatePoints, validateOrder, validate_delete_product,validate_delete_order
from src.models.ecosmart import get_categories , update_rewards_by_user_id, get_rewards_by_user_id, get_reclying_centers
from src.models.product import insert_product, gets_products_by_user_id, delete_product_by_user_id
from src.models.order import create_order, insert_order_items, get_orders_user_id, delete_order_by_user_id, select_order_by_id,delete_materials_by_user_id, select_ids_from_order_items
from flask_jwt_extended import get_jwt_identity, jwt_required
import json

api = Blueprint('api', __name__)

@api.route('/product', methods=['POST'])
@jwt_required()
def create_product():
    user = get_jwt_identity()
    
    isValid = validateProduct( request )
    
    if not isValid[0]:
        return jsonify({"ok":False,'message': isValid[1]}), 400

    image_response = upload_image_to_cloudinary(request.files['image'])
    
    if not image_response['success']:
        return jsonify({"ok":False,'message': image_response["message"]}), 500
    
    image_url = image_response['secure_url']
    
    category = int(request.form['category'])
    
    insert_response = insert_product(image_url,request.form['name'], request.form['description'],category,user['id'])
    
    if not insert_response['success']:
        return jsonify({"ok":False,'message': insert_response["message"]}), 500
    
    return jsonify({"ok":True,'message': insert_response["message"]}), 201

@api.route('/product', methods=['GET'])
@jwt_required()
def get_products_by_user_id():
    user= get_jwt_identity()
    
    materials = gets_products_by_user_id(user['id'])
    
    if materials['success'] == False:
        return jsonify({"ok":False,'message': materials["message"]}), 500
   
    return jsonify({"ok":True,'materials': materials["products"]}), 200

@api.route('/product', methods=['DELETE'])
@jwt_required()
def delete_product():
    user = get_jwt_identity()
    body = request.get_json()
    isValid = validate_delete_product(body)
    
    if not isValid[0]:
        return jsonify({"ok":False,'message': isValid[1]}), 400
    
    response = delete_product_by_user_id(user["id"],body['material_id'])
    
    if not response['success']:
        return jsonify({"ok":False,'message': response["message"]}), 500
    
    if not response["message"]:
        return jsonify({"ok":False,'message': "Product not found"}), 404
    
    return jsonify({"ok":True,'message': "product deleted"}), 200



@api.route('/category', methods=['GET'])
def get_all_categories():
    
    response = get_categories()
    
    if response['success'] == False:
        return jsonify({"ok":False,'message': response["message"]}), 500
    
    return jsonify({"ok":True,'categories':response["categories"]}), 200


@api.route('/centers', methods=['GET'])
def get_centers():
   
   response = get_reclying_centers()
   
   if response['success'] == False:
        return jsonify({"ok":False,'message': response["message"]}), 500
    
   return jsonify({"ok":True,'centers':response["centers"]}), 200



@api.route('/order', methods=['POST'])
@jwt_required()
def create():
    user = get_jwt_identity()
    request_data = request.get_json()
    isValid = validateOrder(request_data)
    if not isValid[0]:
        return jsonify({"ok":False,'message': isValid[1]}), 400
    
    materials = request_data['materials']
    order_response = create_order(user['id'])
    
    if order_response['success'] == False:
        return jsonify({"ok":False,'message': order_response["message"]}), 500
    
    response = process_order_items(materials,int(order_response['order_id']),insert_order_items,int(user['id']))
    
    if response['success'] == False:
        return jsonify({"ok":False,'message': response["message"]}), 500
    
    
    return jsonify({"ok":True,'order_id': order_response['order_id']}), 201


@api.route('/order', methods=['GET'])
@jwt_required()
def get_orders_by_user_id():
    user = get_jwt_identity()
    
    response = get_orders_user_id(user['id'])
    
    if response['success'] == False:
        return jsonify({"ok":False,'message': response["message"]}), 500

    formatted_response = []
    for order in response["orders"]:
        formatted_response.append({
            "order_id": order["order_id"],
            "center_name": order["center_name"],
            "materials": json.loads(order["materials"]) 
        })
    
    return jsonify({"ok":True,'orders': formatted_response}), 200

@api.route('/complete-order', methods=['DELETE'])
@jwt_required()
def complete_order():
    user = get_jwt_identity()
    body = request.get_json()
    isValid = validate_delete_order(body)
    
    if not isValid[0]:
        return jsonify({"ok":False,'message': isValid[1]}), 400
    
    order_exist = select_order_by_id(user['id'],body['order_id'])
    
    if not order_exist['success']:
        return jsonify({"ok":False,'message': "Error deleting order"}), 500
    
    if not order_exist["message"]:
        return jsonify({"ok":False,'message': "Order not found"}), 404
    
    materials = select_ids_from_order_items(body["order_id"],user["id"])
    
    if not materials['success']:
        return jsonify({"ok":False,'message': "Error deleting order" + delete_material["message"]}), 500
    
    material_ids = [material['material_id'] for material in materials["ids"]]
    
    response = delete_order_by_user_id(user["id"],body["order_id"])
    
    if not response['success']:
        return jsonify({"ok":False,'message': "Error deleting order" + delete_material["message"]}), 500
    
    if material_ids:
     format_strings = ','.join(['%s'] * len(material_ids))
     delete_material = delete_materials_by_user_id(format_strings,material_ids)
     
    if not delete_material['success']:
        return jsonify({"ok":False,'message': "Error deleting order" + delete_material["message"]}), 500
    
    return jsonify({"ok":True,'message': "Order deleted"}), 200


@api.route('/order', methods=['DELETE'])
@jwt_required()
def detele_order():
    user = get_jwt_identity()
    body = request.get_json()
    isValid = validate_delete_order(body)

    if not isValid[0]:
        return jsonify({"ok":False,'message': isValid[1]}), 400
    
    response = delete_order_by_user_id(user["id"],body["order_id"])
    
    if not response['success']:
        return jsonify({"ok":False,'message': response["message"]}), 500
    
    if not response["message"]:
        return jsonify({"ok":False,'message': "Order not found"}), 404
    
    return jsonify({"ok":True,'message': "Order deleted"}), 200



@api.route('/rewards', methods=['PUT'])
@jwt_required()
def update_rewards():
    user = get_jwt_identity()
    body = request.get_json()
    
    isValid = validatePoints(body)
    
    if not isValid[0]:
        return jsonify({"ok":False,'message': isValid[1]}), 400
    
    have_points = get_rewards_by_user_id(user['id'])
    
    if have_points['success']:
        if have_points["rewards"]:
            query = "UPDATE rewards SET ammount = %s WHERE user_id = %s"
            response = update_rewards_by_user_id(user['id'],body['ammount'],query)
        else:
            query = "INSERT INTO rewards (ammount,user_id) VALUES (%s, %s)"
            response = update_rewards_by_user_id(user['id'],body['ammount'],query)
    
    if response['success'] == False:
        return jsonify({"ok":False,'message': response["message"]}), 500
    
    return jsonify({"ok":True,'message': response["message"]}), 200


@api.route('/rewards', methods=['GET'])
@jwt_required()
def get_rewards():
    user = get_jwt_identity()
    response = get_rewards_by_user_id(user['id'])
    
    if response['success'] == False:
        return jsonify({"ok":False,'message': response["message"]}), 500
    
    if not response["rewards"]:
        return jsonify({"ok":True,'rewards': 0}), 200
    
    rewards = response["rewards"].get('ammount')
    return jsonify({"ok":True, "rewards": rewards}), 200

