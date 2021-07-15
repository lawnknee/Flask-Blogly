"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

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

# Handle user routes

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
    
    first = request.form['first']
    last = request.form['last']
    image = request.form['img-url'] or None
    
    User.add_new_user(first, last, image)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Shows information about the given user,
    with option to edit or delete the user."""
    
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    
    return render_template('user_detail.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_info(user_id):
    """Shows the edit page for a user.
    Cancel button returns to details page for the user,
    and Save button updates the user information."""
    
    user = User.query.get_or_404(user_id)
    
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_user_edit(user_id):
    """Processes the edit form and returns user to the
    /users page with updated user listing."""
    
    first = request.form['fn']
    last = request.form['ln']
    image = request.form['img'] or None
    
    user = User.query.get_or_404(user_id)
    
    user.first_name = first
    user.last_name = last
    user.image_url = image
    
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes the user and redirects back to main page."""
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')

# Handle Posts

@app.route('/users/<user_id>/posts/new')
def show_post_form(user_id):
    """Shows add post form to user."""
    
    user = User.query.get_or_404(user_id)
    return render_template('user_post.html',user=user)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def submit_post_form(user_id):
    """Handles submitting new post form.
    Adds post to database and redirects to user detail page."""

    # get responses from form
    post_title = request.form['title']
    post_content = request.form['content']

    # update database
    user_post = Post(title=post_title,
                     content=post_content, 
                     user_id=user_id)
    db.session.add(user_post)
    db.session.commit()    

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Shows details about a post with buttons to 
    edit or delete current post. (post view)"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id 
    user = User.query.get_or_404(user_id)
    
    return render_template('user_post_detail.html', user=user, post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Shows form to edit a post. (edit view)
    Hitting cancel returns to post view."""

    post = Post.query.get_or_404(post_id)
    return render_template('user_post_edit.html',post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_submit(post_id):
    """Handles changes made to a existing post. 
    Updates the post in the database and redirects 
    back to post view."""

    # get form  values
    post_title = request.form['title']
    post_content = request.form['content']
    
    # update post
    post = Post.query.get_or_404(post_id)
    post.title = post_title
    post.content = post_content

    db.session.commit()
    
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes the current post and redirects back to
    user details page."""
    
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id 
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')