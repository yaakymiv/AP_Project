from flask import redirect, url_for, render_template, request
from flask_login import login_required, login_user,login_manager,current_user,logout_user
import app
from .models import User, Event, UserEvent, db

#USER

def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.user_profile'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            return render_template('409.html')
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

    return render_template('register.html')

def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('user.user_profile'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            if user.is_admin: 
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('user.user_profile'))
        else:
            return render_template('400.html')

    return render_template('login.html')


@login_required
def user_profile():
    if request.method == 'POST':
        db.session.delete(current_user)
        db.session.commit()

        return redirect(url_for('auth.login'))  

    return render_template('user_profile.html', user=current_user)

@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('auth.login'))
    else:
        return render_template('logout_confirmation.html', user=current_user)
    
@login_required
def profileEvents():
    return render_template('user_events.html', user=current_user)

@login_required
def createEvent():
    data = request.form
    new_event = Event(
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
    )

    user_event = UserEvent(user=current_user, event=new_event)
    db.session.add(user_event)
    db.session.commit()

    return redirect(url_for('user.profileEvents'))

@login_required
def profileEvent(event_id):
    user_event = UserEvent.query.filter_by(user_id=current_user.id, event_id=event_id).first()

    if user_event:
        action = request.form.get('action')

        if action == 'update' and request.method == 'POST':
          
            title = request.form.get('title')
            description = request.form.get('description')
            date = request.form.get('date')

            user_event.event.title = title
            user_event.event.description = description
            user_event.event.date = date

            db.session.commit()
            return redirect(url_for('user.profileEvent',event_id=event_id))

        elif action == 'delete' and request.method == 'POST':
            
            db.session.delete(user_event)
            db.session.commit()
            return redirect(url_for('user.profileEvents',event_id=event_id))
        elif action=='add' and request.method == 'POST':
                
                participant_username = request.form.get('participant_username')

                participant_user = User.query.filter_by(username=participant_username).first()

                if participant_user:
                    # Check if the user is already a participant
                    if participant_user not in [participant.user for participant in user_event.event.event_users]:
                        # Add the user as a participant
                        new_participant = UserEvent(user=participant_user, event=user_event.event)
                        db.session.add(new_participant)
                        db.session.commit()

                # Redirect back to the event details page
                return redirect(url_for('user.profileEvent', event_id=event_id))
        else:
            # Render the template for the initial GET request
            return render_template('event.html', user_event=user_event)
    else:
        return render_template('404.html')

    

    
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
