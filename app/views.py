from flask import jsonify, request
from .models import getAllUsers, createUser, getUserById, updateUser, deleteUser, getUserEvents, createEvent, getEventById, updateEvent, deleteEvent

## /users

def get_all_users():
    users = getAllUsers()
    if users:
        return jsonify(users)
    else:
        return jsonify({"error": "Users not found"}), 404

def create_user():
    data = request.json
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    result = createUser(data)
    if result['status']:
        return jsonify(result), 201
    else:
        return jsonify({"error": "User already exists"}), 409


## /users/{user_id}
def get_user_by_id(user_id):
    user = getUserById(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

def update_user(user_id):
    data = request.json
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    result = updateUser(user_id, data)
    if result:
        return jsonify(result), 201
    else:
        return jsonify({"error": "User not found"}), 404

def delete_user(user_id):
    result = deleteUser(user_id)
    if result:
        return '', 204
    else:
        return jsonify({"error": "User not found"}), 404

## /users/{user_id}/events

def get_user_events(user_id):
    events = getUserEvents(user_id)
    if events:
        return jsonify({"events": events})
    else:
        return jsonify({"error": "User not found or no events associated"}), 404

def create_event(user_id):
    data = request.json
    if 'title' not in data or 'description' not in data or 'date' not in data or 'users' not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    result = createEvent(user_id, data)
    if result['status']:
        return jsonify(result), 201
    else:
        return jsonify({"error": "Invalid request payload"}), 400

## users/user_id/events/event_id

def get_event_by_id(user_id, event_id):
    event = getEventById(user_id, event_id)
    if event:
        return jsonify(event)
    else:
        return jsonify({"error": "Event not found"}), 404

def update_event(user_id, event_id):
    data = request.json
    if 'title' not in data or 'description' not in data or 'date' not in data or 'users' not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    result = updateEvent(user_id, event_id, data)
    if result:
        return jsonify(result), 201
    else:
        return jsonify({"error": "Event not found"}), 404

def delete_event(user_id, event_id):
    result = deleteEvent(user_id, event_id)
    if result:
        return '', 204
    else:
        return jsonify({"error": "Event not found"}), 404
