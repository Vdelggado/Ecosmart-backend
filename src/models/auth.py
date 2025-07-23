from ..db.db_mysql import get_db_connection

def select_user_by_email(email):
    try: 
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id,name,password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "user":user
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": "Error consulting the database"
            }

def insert_user(name, lastname, email, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, lastname, email, password) VALUES (%s, %s, %s, %s)", (name, lastname, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "message": "User created"
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error inserting the user"
        }

def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, lastname, email FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "success": True,
            "user": user
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error getting user" + " " + str(e)
        }