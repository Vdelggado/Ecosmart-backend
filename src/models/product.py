from ..db.db_mysql import get_db_connection

def insert_product(image,name, description,category,user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO materials (image,name, description,category_id,user_id) VALUES (%s, %s, %s,%s,%s)", (image,name, description,category, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "message": "product created"
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error creating product" + str(e)
        }
        
def gets_products_by_user_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                m.material_id,
                m.image,
                m.name,
                m.description,
                c.name AS category_name
            FROM 
                materials m
            JOIN 
                category c ON m.category_id = c.category_id
            WHERE 
                m.user_id = %s;
            """
        cursor.execute(query, (user_id,))
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "products": products
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error getting products" 
        }
        
def delete_product_by_user_id(user_id, material_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        response = cursor.execute("DELETE FROM materials WHERE  material_id = %s  AND user_id = %s ", (material_id,user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "message": response
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error deleting product" +" "+ str(e)
        }