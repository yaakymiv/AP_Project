from flask import Flask
from .url import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp, url_prefix='/api')

from app import views

