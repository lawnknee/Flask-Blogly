"""Seed file to make sample data for Users and Posts"""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
loni = User(first_name='Loni', last_name='Kuang', image_url='https://rithm-students-media.s3.amazonaws.com/CACHE/images/user_photos/loni-kuang/0bca5f22-fd55-4371-9eda-938d8d66ef53-profile/f62d8ba33b4d110ff875b3bdd6de2848.jpg')
ray = User(first_name='Ray', last_name='Agni', image_url='https://rithm-students-media.s3.amazonaws.com/CACHE/images/user_photos/jhensen-agni/6a11f561-4a5a-4e77-a759-929a9f37f766-37388027/2cfc9e8d67110fecb58ff8d62d99b668.jpeg')
bob = User(first_name='Bob', last_name='Smith')

# Add new user objects to session, so they'll persist
db.session.add(loni)
db.session.add(ray)
db.session.add(bob)

# Commit--otherwise, this never gets saved!
db.session.commit()

# Add posts
post1 = Post(title='Breaking News!', content='New Coding Language Found!', user_id=1)
post2 = Post(title='')

# Add new post objects to session, so they'll persist
db.session.add(post1)
db.session.commit()