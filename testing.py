from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class FlaskTestsBasic(TestCase):
    """Flask tests."""
    
    def setUp(self):
        """Do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_index(self):
        """Test homepage."""

        result = self.client.get("/")
        self.assertIn(b"Welcome", result.data)
    
    def test_logout(self):
        """Test logout route."""
        with self.client as c:
            with c.session_transaction as sess:
                sess['user_email'] = 'jerry@test.com'
            
            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_email', session)
            self.assertIn(b'logged out', result.data)

class FlaskTestsDatabase(TestCase):
    """Tests that use the database."""
    
    def setUp(self):
        """Do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

    def tearDown(self):
        """Do at the end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login(self):
        """Test login route."""

        result = self.client.post("/login", data={"email": "jerry@test.com", "password": "test"}, follow_redirects=True)
        self.assertIn(b"Welcome back", result.data)
    
class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged into session."""

    def setUp(self):
        """Do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction as sess:
                sess['user_email'] = "jerry@test.com"
    
    def test_dashboard(self):
        """Test user dashboard page."""

        result = self.client.get("/user_dashboard")
        self.assertIn(b"here's your dashboard", result.data)
