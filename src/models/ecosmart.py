from ..db.db_mysql import get_db_connection

def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT category_id, name FROM category")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "categories": categories
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error getting categories"
        }
             
def update_rewards_by_user_id(user_id, points, query):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (points, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "message": "rewards updated"
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error updating rewards" + str(e)
        }
        
def get_rewards_by_user_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ammount FROM rewards WHERE user_id = %s", (user_id,))
        rewards = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "rewards": rewards
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error getting rewards"
        }
def get_reclying_centers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT center_id, name, location, phone FROM recycling_center")
        centers = cursor.fetchall()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "centers": centers
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error getting centers" 
        }