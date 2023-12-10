from flask import Blueprint
from .views import user_profile,register,login,logout,profileEvents,profileEvent,getAllUsers, getUserById, updateUser, deleteUser, getUserEvents, createEvent, getEventById, createUser

auth_bp = Blueprint('auth', __name__)

auth_bp.add_url_rule('/login',view_func=login,methods=['GET','POST'])
auth_bp.add_url_rule('/register',view_func=register,methods=['GET','POST'])
auth_bp.add_url_rule('/profile/logout',view_func=logout,methods=['GET','POST'])

user_bp = Blueprint('user', __name__)

user_bp.add_url_rule('/profile',view_func=user_profile,methods=['GET','POST'])
user_bp.add_url_rule('/profile/events',view_func=profileEvents,methods=['GET'])
user_bp.add_url_rule('/profile/events',view_func=createEvent,methods=['POST'])
user_bp.add_url_rule('/profile/events/<int:event_id>',view_func=profileEvent,methods=['GET','POST'])