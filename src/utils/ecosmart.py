import cloudinary.uploader

def upload_image_to_cloudinary(image):
    try:
        image_response = cloudinary.uploader.upload(image)
        return {
            "success": True,
            "secure_url": image_response['secure_url']
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": str("Error uploading image")
        }

def delete_image_from_cloudinary(image_url):
    try:
        image_response = cloudinary.uploader.destroy(image_url)
        return {
            "success": True,
            "secure_url": image_response['secure_url']
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": "Error deleting image"
        }



def process_order_items(materials,order_id,func,user_id):
    for material in materials:
        response = func(order_id,material['material_id'],material['center_id'],user_id)
        if not response['success']:
            return {
            "success": False,
            "message": response["message"]
        }

    return {
        "success": True,
        "message": "Order created successfully"
    }