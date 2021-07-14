from unittest import TestCase

from app import app

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UserTestCase(TestCase):

	def test_main_page(self):
		""" Tests if main page redirects to /users"""
		with app.test_client() as client:
			# checks for redirect and if page loads list of users
			resp = client.get('/', follow_redirects=True)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('User Listing', html)
	
	def test_add_user(self):
		"""Tests if add-new user redirects to /users/new"""
		with app.test_client() as client:
			resp = client.get('/users/new')
			html = resp.get_data(as_text=True)  

			self.assertEqual(resp.status_code, 200)
			self.assertIn("Create User Form", html)

	def test_add_user_submit(self):

		with app.test_client() as client:
			data = {'first':"Idk", "last":"MyName", "img-url": "somerandomURL"}
			resp = client.post('/users/new',data=data, follow_redirects=True)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('User Listing', html)