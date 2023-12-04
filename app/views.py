from flask import render_template, request
from .models import User, Event, UserEvent, db

# /users

def getAllUsers():
    users = User.query.all()
    if not users:
        return render_template('404.html'), 404
    return render_template('user_list.html', users=users)

def createUser():
    data = request.json
    if not data:
        return render_template('400.html'), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter((User.username == username) | (User.email == email)| (User.password == password)).first()

    if existing_user:
        return render_template('409.html', entity='User'),409

    new_user = User(
        username=username,
        email=email,
        password=password
    )

    db.session.add(new_user)
    db.session.commit()

    return render_template('new_user.html', userId=new_user.id, username=new_user.username),201

# /users/{user_id}

def getUserById(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('user.html', user=user)
    else:
        return render_template('404.html'), 404

def updateUser(user_id):
    user = User.query.get(user_id)
    data = request.json
    if not data:
        return render_template('400.html'), 400

    if user:
        user.username = data.get('username')
        user.email = data.get('email')
        user.password = data.get('password')

        db.session.commit()

        return render_template('new_user.html', userId=user.id, username=user.username),201
    else:
        return render_template('404.html'), 404

def deleteUser(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return render_template('delete.html', Id=user.id,entity='User'),204
    else:
        return render_template('404.html'), 404

# /users/{user_id}/events

def getUserEvents(user_id):
    user = User.query.get(user_id)
    if user:
        events = user.events
        return render_template('user_events.html', user=user, events=events),200
    else:
        return render_template('404.html'), 404

def createEvent(user_id):
    user = User.query.get(user_id)
    data = request.json
    if not data:
        return render_template('400.html'), 400

    if user:
        new_event = Event(
            title=data.get('title'),
            description=data.get('description'),
            date=data.get('date'),
        )

        user_event = UserEvent(user=user, event=new_event)
        db.session.add(user_event)
        db.session.commit()

        return render_template('new_event.html', title=new_event.title,date=new_event.date),201
    else:
        return render_template('404.html'), 404

# users/user_id/events/event_id

def getEventById(user_id, event_id):
    user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
    if user_event:
        return render_template('event.html', user_event=user_event),200
    else:
        return render_template('404.html'), 404
    
def updateEvent(user_id, event_id):
    user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
    data = request.json
    if not data:
        return render_template('400.html'), 400

    if user_event:
        event = user_event.event
        event.title = data.get('title')
        event.description = data.get('description')
        event.date = data.get('date')

        db.session.commit()

        return render_template('new_event.html', title=user_event.event.title,date=user_event.event.date),201
    else:
        return render_template('404.html'), 404

def deleteEvent(user_id, event_id):
    user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()

    if user_event:
        db.session.delete(user_event)
        db.session.commit()
        return render_template('delete.html', Id=event_id,entity='Event'),204
    else:
        return render_template('404.html'), 404
    
def seed_data():
    # Test Data for User model
    user_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'password': 'pass123'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'pass456'},
        {'username': 'bob_miller', 'email': 'bob@example.com', 'password': 'pass789'},
        {'username': 'alice_jones', 'email': 'alice@example.com', 'password': 'passabc'},
        {'username': 'charlie_brown', 'email': 'charlie@example.com', 'password': 'passdef'},
    ]

    # Test Data for Event model
    event_data = [
        {'title': 'Party Night', 'description': 'Join us for a night of fun!', 'date': '2023-12-01 20:00:00'},
        {'title': 'Tech Conference', 'description': 'Explore the latest in technology.', 'date': '2023-11-15 09:00:00'},
        {'title': 'Book Club Meeting', 'description': 'Discussing the latest bestseller.', 'date': '2023-11-10 18:30:00'},
        {'title': 'Fitness Class', 'description': 'Get fit with our workout sessions.', 'date': '2023-11-20 17:00:00'},
        {'title': 'Game Night', 'description': 'Play board games and have fun!', 'date': '2023-12-05 19:00:00'},
    ]

    # Test Data for UserEvent model
    user_event_data = [
        {'user_id': 1, 'event_id': 1},
        {'user_id': 2, 'event_id': 3},
        {'user_id': 3, 'event_id': 2},
        {'user_id': 4, 'event_id': 5},
        {'user_id': 5, 'event_id': 4},
    ]

    for user_info in user_data:
        user = User(**user_info)
        db.session.add(user)

    for event_info in event_data:
        event = Event(**event_info)
        db.session.add(event)

    for user_event_info in user_event_data:
        user_event = UserEvent(**user_event_info)
        db.session.add(user_event)

    db.session.commit()
