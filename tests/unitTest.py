import unittest
from werkzeug.security import generate_password_hash
import sys
import os

# Add parent directory to path to import app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from config import TestingConfig

class CalTrackUnitTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Test client
        self.client = self.app.test_client()
        
        # Create tables and seed test data
        db.create_all()
        
        # Seed one user with known password
        u = User(
            username='alice',
            email='alice@example.com',
            password_hash=generate_password_hash('Secret123')
        )
        db.session.add(u)
        db.session.commit()
        self.email = u.email
        self.password = 'Secret123'

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_database_connection(self):
        # Check if the database is connected
        self.assertIsNotNone(db.engine)
        # Check if the User table exists
        self.assertTrue(db.engine.dialect.has_table(db.engine, 'user'))
            
    def test_index_renders_login(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Welcome to CalTrack', r.data)

    def test_login_with_bad_password_redirects(self):
        r = self.client.post('/login', data={
            'email': self.email,
            'password': 'wrong'
        }, follow_redirects=False)
        self.assertEqual(r.status_code, 302)
        self.assertIn('/index', r.headers['Location'])

    def test_login_with_good_credentials_redirects_home(self):
        r = self.client.post('/login', data={
            'email': self.email,
            'password': self.password
        }, follow_redirects=False)
        self.assertEqual(r.status_code, 302)
        self.assertIn('/home', r.headers['Location'])

    def test_protected_home_requires_login(self):
        r = self.client.get('/home', follow_redirects=False)
        self.assertEqual(r.status_code, 302)
        self.assertIn('/index', r.headers['Location'])

    def test_protected_home_after_login(self):
        # first log in
        self.client.post('/login', data={
            'email': self.email,
            'password': self.password
        }, follow_redirects=False)
        # then /home should load
        r = self.client.get('/home')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Your Calorie Tracking Overview', r.data)

    def test_logout_clears_session(self):
        # log in
        self.client.post('/login', data={
            'email': self.email,
            'password': self.password
        }, follow_redirects=False)
        # hit logout
        r = self.client.get('/logout', follow_redirects=False)
        self.assertEqual(r.status_code, 302)
        self.assertIn('/index', r.headers['Location'])
        # subsequently protected should redirect again
        r2 = self.client.get('/home', follow_redirects=False)
        self.assertEqual(r2.status_code, 302)
