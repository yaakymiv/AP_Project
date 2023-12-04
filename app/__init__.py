import json
from flask import Flask
from .url import users_bp
from .models import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost/calendar'
app.register_blueprint(users_bp, url_prefix='/api')

db.init_app(app)
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
        return super().default(obj)
    
app.json_encoder = CustomJSONEncoder
migrate = Migrate(app, db)

