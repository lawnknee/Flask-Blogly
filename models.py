"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_URL = 'https://rithm-students-media.s3.amazonaws.com/CACHE/images/user_photos/brit/480dfb17-4431-4d8d-86f9-6c85b6571e7b-brit/819782924da7552d2e53d3d14da53865.jpeg'

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