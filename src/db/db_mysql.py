from pymysql import connect, cursors
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return connect (
        host=getenv("MYSQL_HOST"),
        user=getenv("MYSQL_USER"),
        password = getenv("MYSQL_PASSWORD"),
        db=getenv("MYSQL_DB"),
        port=int(getenv("MYSQL_PORT")),
        cursorclass=cursors.DictCursor
    )

