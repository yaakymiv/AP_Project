from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()

db = SQLAlchemy(model_class=Base)

class UserEvent(db.Model):
    __tablename__ = 'user_event'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.eventId'), primary_key=True)

    user = relationship('User', back_populates='user_events')
    event = relationship('Event', back_populates='event_users')

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    user_events = relationship('UserEvent', back_populates='user')

    def events(self):
        return [user_event.event for user_event in self.user_events]

class Event(db.Model):
    __tablename__ = 'events'

    eventId = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, default=func.now())

    event_users = relationship('UserEvent', back_populates='event')
