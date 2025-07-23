from flask_jwt_extended import create_access_token
from datetime import timedelta
def create_jwt_token(id,name):
    return create_access_token(identity={'id':id,'name':name}, expires_delta=timedelta(minutes=60))
