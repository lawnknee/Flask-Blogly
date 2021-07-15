from unittest import TestCase

from sqlalchemy.sql.operators import as_
from app import app
from models import db, User, Post 

# Test database (don't want to mess up our real database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# NOTE: why do we need to move db.drop_all() and db.create_all() into the class

class UserTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()
        User.query.delete()
        test_user = User(first_name="test_first_name", 
                        last_name="test_last_name", 
                        image_url="")
        db.session.add(test_user)
        db.session.commit()
        
        self.test_user = test_user
    
    def test_main_page(self):
        """ Tests if main page redirects to /users"""
        with app.test_client() as client:
            # checks for redirect and if page loads list of users
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User Listing', html)

    def test_add_user(self):
        """Tests if add-new-user form loads."""
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)  

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create User Form", html)

    def test_add_user_submit(self):
        """Tests if adding a new user redirects to /users page."""

        with app.test_client() as client:
            data = {'first':f"{self.test_user.first_name}", 
                    "last":f"{self.test_user.last_name}", 
                    "img-url": f"{self.test_user.image_url}"}
            resp = client.post('/users/new',data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{data["first"]} {data["last"]}', html)
            
    def test_show_edit_page(self):
        """Tests if edit user info page loads."""
        
        with app.test_client() as client:
            resp = client.get(f'/users/{self.test_user.id}/edit') # don't wan't to hard code an ID, refer to test_user on setUp
            html = resp.get_data(as_text=True) 
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit User Form', html)


class PostTestCase(TestCase):
    """Test cases for post routing and updates"""

    def setUp(self):
        """ Creates test users and test posts"""

        db.drop_all()
        db.create_all()
        User.query.delete()
        self.test_user = User(first_name="test_first_name",
                        last_name="test_last_name", image_url="")
        db.session.add(self.test_user)
        db.session.commit()

        # create a test db
        Post.query.delete()
        self.test_post = Post(title="test_title", 
                        content="test_content", 
                        user_id=self.test_user.id)
        db.session.add(self.test_post)
        db.session.commit()
        
    
    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()
    
    def test_show_post_form(self):
        """Tests if add new post form loads."""
        
        with app.test_client() as client:
            resp = client.get(f'/users/{self.test_user.id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User New Post Form', html)
            # test invalid user_id route to 404
    
    def test_submit_post_form(self):
        """Tests if new post was successfully submitted."""
        
        with app.test_client() as client:
            data = {
                "title": self.test_post.title, 
                "content": self.test_post.content,
                "user_id": self.test_post.user_id
            }
            resp = client.post(f'/users/{self.test_user.id}/posts/new', 
                                data=data, 
                                follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            # checks for redirect 
            self.assertEqual(resp.status_code, 200)
            self.assertIn('User Detail Page ', html)
            
            # check for valid updates
            self.assertIn(f'{data["title"]}', html)
            
    def test_post_details(self):
        """Tests if post details page loads."""
        
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.test_post.id}')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post Details Page', html)
            self.assertIn(f'{self.test_post.title}', html)
            
    def test_edit_post(self):
        """Tests if edit post page loads."""
        
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.test_post.id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Post Page', html)
            self.assertIn(f'{self.test_post.title}', html)
            
    def test_edit_post_submit(self):
        """Tests if edited post routes back to post view page,
        with edited post."""

        with app.test_client() as client:
            data = {
                "title": 'new_test_title', 
                "content": 'new_test_content',
                "user_id": self.test_post.user_id
            }
            resp = client.post(f'/posts/{self.test_post.id}/edit', 
                               data=data,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post Details Page', html)
            self.assertIn(f'{data["title"]}', html)
            self.assertIn(f'{data["content"]}', html)
        
    def test_delete_post(self):
        """Tests if current post gets deleted and user gets 
        redirected back to user details page."""

        with app.test_client() as client:
            resp = client.get(f'/posts/{self.test_post.id}/delete',
                              follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User Detail Page', html)
            self.assertNotIn(f'{self.test_post.title}', html)
