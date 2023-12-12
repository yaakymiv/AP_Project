from flask import abort, redirect, url_for, render_template, request
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
            abort(409)
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
            abort(404)

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
                    if participant_user not in [participant.user for participant in user_event.event.event_users]:
                        new_participant = UserEvent(user=participant_user, event=user_event.event)
                        db.session.add(new_participant)
                        db.session.commit()

                return redirect(url_for('user.profileEvent', event_id=event_id))
        else:
            return render_template('event.html', user_event=user_event)
    else:
        abort(404)

