"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_URL = 'https://lorempixel.com/400/400/cats/'

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """User."""
  
    __tablename__ = "users"
  
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text,
                          default=DEFAULT_URL)
    # NOTE: why doesn't it work 
    # posts = db.relationship('Post', backref='user')

    
    @classmethod
    def add_new_user(cls, first, last, image):
        # if image == "":
        #     image = default_url
        
        # image = image if (image) else DEFAULT_URL
        

        new_user = cls(first_name=first, last_name=last, image_url=image)
        db.session.add(new_user)
        # db.session.commit() 
        # should never commit in method
        # always commit in the view function to close out the transaction

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
