from flask import Blueprint
from .views import getAllUsers, getUserById, updateUser, deleteUser, getUserEvents, createEvent, getEventById, createUser, updateEvent, deleteEvent

users_bp = Blueprint('users', __name__)

users_bp.add_url_rule('/users', view_func=getAllUsers, methods=['GET'])
users_bp.add_url_rule('/users', view_func=createUser, methods=['POST'])

users_bp.add_url_rule('/users/<int:user_id>', view_func=getUserById, methods=['GET'])
users_bp.add_url_rule('/users/<int:user_id>', view_func=updateUser, methods=['PUT'])
users_bp.add_url_rule('/users/<int:user_id>', view_func=deleteUser, methods=['DELETE'])

users_bp.add_url_rule('/users/<int:user_id>/events', view_func=getUserEvents, methods=['GET'])
users_bp.add_url_rule('/users/<int:user_id>/events', view_func=createEvent, methods=['POST'])

users_bp.add_url_rule('/users/<int:user_id>/events/<int:event_id>', view_func=getEventById, methods=['GET'])
users_bp.add_url_rule('/users/<int:user_id>/events/<int:event_id>', view_func=updateEvent, methods=['PUT'])
users_bp.add_url_rule('/users/<int:user_id>/events/<int:event_id>', view_func=deleteEvent, methods=['DELETE'])
