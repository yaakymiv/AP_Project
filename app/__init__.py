import json
from flask import Flask, redirect, request, url_for
from app.views import login
from .url import auth_bp,user_bp
from flask_login import LoginManager, current_user
from .models import db,User,UserEvent,Event
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__,template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost/calendar'
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login_view'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class CustomView(ModelView):

    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
    
class UserEventView(CustomView):
    column_list = ('user', 'event')
    column_labels = {
        'user': 'User',
        'event': 'Event',
    }
    
    form_columns = ('user', 'event')

    form_ajax_refs = {
        'user': {
            'fields': (User.username,),
        },
        'event': {
            'fields': (Event.title,),
        }
    }

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(CustomView(User, db.session, endpoint='admin_user'))
admin.add_view(UserEventView(UserEvent, db.session, endpoint='admin_user_event'))
admin.add_view(CustomView(Event, db.session, endpoint='admin_event'))
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


