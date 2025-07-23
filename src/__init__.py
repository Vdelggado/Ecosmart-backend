from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import getenv
from dotenv import load_dotenv
import cloudinary

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

cloudinary.config( 
  cloud_name = getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = getenv('CLOUDINARY_API_KEY'),
  api_secret = getenv('CLOUDINARY_API_SECRET'),
  secure=True
)

from .routes.auth import auth
from .routes.ecosmart import api

def init_app():
    app.register_blueprint(auth , url_prefix='/auth')
    app.register_blueprint(api , url_prefix='/api')
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    return app