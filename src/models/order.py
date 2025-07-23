from ..db.db_mysql import get_db_connection
def create_order(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (user_id,))
        order_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "order_id": order_id
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error creating order" +" "+ str(e)
        }

def insert_order_items(order_id, material_id, center_id,user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO order_items (order_id, material_id, center_id,user_id) VALUES (%s, %s, %s, %s)", (order_id, material_id, center_id,user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "message": "order item created"
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error creating order" + str(e)
        }
        
def get_orders_user_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor() 
        query = """
            SELECT 
            o.order_id,
            ce.name AS center_name,
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    "material_id", oi.material_id,
                    "name", m.name,
                    "description", m.description,
                    "image", m.image,
                    "category_name", c.name
                )
            ) AS materials
            FROM 
                orders o
            JOIN 
                order_items oi ON o.order_id = oi.order_id
            JOIN 
                materials m ON oi.material_id = m.material_id
            JOIN 
                category c ON m.category_id = c.category_id
            JOIN
                recycling_center ce ON oi.center_id = ce.center_id
            WHERE 
                o.user_id = %s
            GROUP BY 
                o.order_id, ce.name;
            """
        cursor.execute(query, (user_id,))
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "orders": orders
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error getting orders"
        } 
        
def delete_order_by_user_id(user_id, order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        response = cursor.execute("DELETE FROM orders WHERE  order_id = %s  AND user_id = %s ", (order_id,user_id))
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
            "message": " "+ str(e)
        }
        
def select_order_by_id(user_id, order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        response = cursor.execute("select order_id, user_id from orders WHERE  order_id = %s  AND user_id = %s ", (order_id,user_id))
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
            "message": " " + str(e)
        }

def select_ids_from_order_items(order_id, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT material_id FROM order_items WHERE order_id = %s AND user_id = %s", (order_id,user_id))
        ids = cursor.fetchall()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "ids": ids
        }
    except Exception as e:
        return {
            "success": False,
            "message": " " + str(e)
        }
   
def delete_materials_by_user_id(format_strings,material_ids):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM materials WHERE material_id IN ({format_strings})"
        response = cursor.execute(query, material_ids)
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
            "message": " "+ str(e)
        }