from flask import Blueprint
from .views import get_all_users, get_user_by_id,update_user,delete_user, get_user_events,create_event, get_event_by_id,create_user,update_event,delete_event

users_bp = Blueprint('users', __name__)

users_bp.add_url_rule('/users', view_func=get_all_users, methods=['GET'])
users_bp.add_url_rule('/users', view_func=create_user, methods=['POST'])

users_bp.add_url_rule('/users/<int:user_id>', view_func=get_user_by_id, methods=['GET'])
users_bp.add_url_rule('/users/<int:user_id>', view_func=update_user, methods=['PUT'])
users_bp.add_url_rule('/users/<int:user_id>', view_func=delete_user, methods=['DELETE'])

users_bp.add_url_rule('/users/<int:user_id>/events', view_func=get_user_events, methods=['GET'])
users_bp.add_url_rule('/users/<int:user_id>/events', view_func=create_event, methods=['POST'])

users_bp.add_url_rule('/users/<int:user_id>/events/<int:event_id>', view_func=get_event_by_id, methods=['GET'])
users_bp.add_url_rule('/users/<int:user_id>/events/<int:event_id>', view_func=update_event, methods=['PUT'])
users_bp.add_url_rule('/users/<int:user_id>/events/<int:event_id>', view_func=delete_event, methods=['DELETE'])


