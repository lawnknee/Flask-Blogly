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
    """Main page redirects to list of users."""
    
    return redirect('/users')
                 
@app.route('/users')
def show_users():
    """Shows all users as links with a button to add a new user. 
    Clicking on the link will go to the user's detail page."""
    
    allUsers = User.query.all()    
    
    return render_template('user_listing.html', users=allUsers)  # TODO: rename user for later

@app.route('/users/new', methods=["GET"])
def show_add_user_form():
    """Shows a form to add a new user."""
    
    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Processes the add new user form.
    Redirects to /users with list of all users."""
    
    first_name = request.form['first']
    last_name = request.form['last']
    image_url = request.form['img-url']
    
    # insert user into user database
    # pull back users and pass into redirect
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Shows information about the given user,
    with option to edit or delete the user."""
    
    # access database using user_id
    
    return render_template('user_detail.html')

@app.route('/users/<int:user_id>/edit')
def edit_user_info(user_id):
    """Shows the edit page for a user.
    Cancel button returns to details page for the user,
    and Save button updates the user information."""
    
    return render_template('user_edit.html')

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_user_edit(user_id):
    """Processes the edit form and returns user to the
    /users page with updated user listing."""
    
    # process edit form
    # update database
    # get updated user info back from database

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes the user and redirects back to main page."""
    
    # delete user from database
    
    return redirect('/')