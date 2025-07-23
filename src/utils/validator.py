
def isEmpty( value ):
    return value == None or value == ""

def validateRegister( name, password, email,lastname):
    if isEmpty( name ):
        return  False,"Name is required"
    if isEmpty( email ):
        return  False,"Email is required"
    if isEmpty( password ):
        return  False,"Password is required"
    if isEmpty( lastname ): 
        return False,"Lastname is required"
    
    return True,""


def validateLogin( email,password):
    if isEmpty( email ):
        return  False,"Email is required"
    if isEmpty( password ):
        return  False,"Password is required"
    return True,""

def validateProduct( request ):
    
    if 'image' not in request.files:
        return  False,"image is required"
    
    if not request.form.get('name'):
        return False,"name is required"
    
    if not request.form.get('description'):
        return False,"description is required"
    
    if not request.form.get('category'):
        return False,"category is required"
    
    if request.files['image'].filename == '':
        return False,"image is empty"
    
    return True,""

def validatePoints( request ):
    ammount = request.get('ammount')
    if not ammount:
        return False,"ammount is required"
    
    if not isinstance(ammount, float):
        return False,"ammount must be a float"
    
    return True,""

def validateOrder( request ):
    materials = request.get('materials')
    if not materials:
        return False,"materials is required"
    if not isinstance(materials, list):
        return False,"materials must be a list"
    if len(materials) == 0:
        return False,"materials is empty"
    
    for material in materials:
        if not material.get('material_id'):
            return False,"material_id is required"
        
        if not material.get('center_id'):
            return False,"center_id is required"
        
        if not isinstance(material['material_id'], int):
            return False,"material_id must be a number"
        
        if not isinstance(material['center_id'], int):
            return False,"center_id must be a number"
        
    return True,""

def validate_delete_product( request ):
    if not request.get('material_id'):
        return False,"material_id is required"
    
    if not isinstance(request['material_id'], int):
        return False,"material_id must be a number"
    
    return True,""

def validate_delete_order( request ):
    if not request.get('order_id'):
        return False,"order_id is required"
    
    if not isinstance(request['order_id'], int):
        return False,"order_id must be a number"
    
    return True,""