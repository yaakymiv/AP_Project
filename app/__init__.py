import json
from flask import Flask, redirect, url_for
from .url import users_bp,auth_bp,user_bp
from flask_login import LoginManager, current_user
from .models import db,User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__,template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost/calendar'
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login_view'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#unauthorized/restricted handler

@login_manager.unauthorized_handler
def unauthorized_callback():
    if current_user.is_authenticated:
        # User is authenticated but doesn't have permission for the requested page
        return redirect(url_for('auth.profile'))  
    else:
        # User is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
        return super().default(obj)
app.json_encoder = CustomJSONEncoder

migrate = Migrate(app, db)


