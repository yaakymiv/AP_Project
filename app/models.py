
import datetime

users_data = [
    {"id": 1, "username": "user1", "email": "user1@example.com", "password": "pass1"},
    {"id": 2, "username": "user2", "email": "user2@example.com", "password": "pass2"}
]

events_data = [
    {
        "user_id": 1,
        "events": [
            {"eventId": 123, "title": "Event 1", "description": "Description of Event 1", "date": "2023-11-17T12:00:00Z"},
            {"eventId": 456, "title": "Event 2", "description": "Description of Event 2", "date": "2023-11-18T14:00:00Z"}
        ]
    },
    {
        "user_id": 2,
        "events": []
    }
]

## /users

def getAllUsers():
    return users_data

def createUser(data):
    username = data.get('username')
    email = data.get('email')

    for user in users_data:
        if user['username'] == username or user['email'] == email:
            return {"error": "User already exists", "status": False}

    new_user = {
        "id": len(users_data) + 1,
        "username": username,
        "email": email,
        "password": data.get('password')
    }

    users_data.append(new_user)
    return {"status": True, "userId": new_user["id"], "username": new_user["username"]}


## /users/{user_id}

def getUserById(user_id):
    for user in users_data:
        if user['id'] == user_id:
            return user
    return None

def updateUser(user_id, data):
    for user in users_data:
        if user['id'] == user_id:
            user['username'] = data.get('username')
            user['email'] = data.get('email')
            user['password'] = data.get('password')
            return {"status": True, "userId": user['id'], "username": user['username']}
    return None

def deleteUser(user_id):
    for i, user in enumerate(users_data):
        if user['id'] == user_id:
            del users_data[i]
            return True
    return False


## /users/{user_id}/events

def getUserEvents(user_id):
    for user_events in events_data:
        if user_events['user_id'] == user_id:
            return user_events.get('events', [])
    return None

def createEvent(user_id, data):
    for user_events in events_data:
        if user_events['user_id'] == user_id:
            new_event = {
                "eventId": len(user_events['events']) + 1,
                "title": data.get('title'),
                "description": data.get('description'),
                "date": data.get('date'),
                "users": data.get('users')
            }
            user_events['events'].append(new_event)
            return {"status": True, "eventId": new_event["eventId"], "title": new_event["title"]}
    return {"status": False}

## users/user_id/events/event_id

def getEventById(user_id, event_id):
    for user_events in events_data:
        if user_events['user_id'] == user_id:
            for event in user_events['events']:
                if event['eventId'] == event_id:
                    return event
    return None

def updateEvent(user_id, event_id, data):
    for user_events in events_data:
        if user_events['user_id'] == user_id:
            for event in user_events['events']:
                if event['eventId'] == event_id:
                    event['title'] = data.get('title')
                    event['description'] = data.get('description')
                    event['date'] = data.get('date')
                    event['users'] = data.get('users')
                    return {"status": True, "eventId": event['eventId'], "title": event['title']}
    return None

def deleteEvent(user_id, event_id):
    for user_events in events_data:
        if user_events['user_id'] == user_id:
            for i, event in enumerate(user_events['events']):
                if event['eventId'] == event_id:
                    del user_events['events'][i]
                    return True
    return False
