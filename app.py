"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route('/')
def main_page():

    return redirect('/users')
                 
@app.route('/users')
def show_users():
    
    return render_template('user_listing.html', user="Someone")  # TODO: rename user for later

@app.route('/users/new', methods=["GET"])
def show_add_user_form():

    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form['first']
    last_name = request.form['last']
    image_url = request.form['img-url']
    
    # insert user into user database
    # pull back users and pass into redirect
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    
    return render_template('user_detail.html')

@app.route('/users/<int:user_id>/edit')
def edit_user_info(user_id):
    
    return render_template('user_edit.html')

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_user_edit(user_id):

    # process edit form
    # update database
    # get updated user info back from database

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    
    # delete user from database
    
    return redirect('/')