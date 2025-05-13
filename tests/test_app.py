import unittest
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import User

class CalTrackUnitTests(unittest.TestCase):
    def setUp(self):
        # In-memory DB & disable CSRF for form posts
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()
        with app.app_context():
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
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_renders_login(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Welcome to CalTrack', r.data)

    def test_login_with_bad_password_redirects(self):
        # /login returns 400 on missing fields :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}
        r = self.client.post('/login', data={
            'email': self.email,
            'password': 'wrong'
        }, follow_redirects=False)
        # redirect back to index on bad creds :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}
        self.assertEqual(r.status_code, 302)
        self.assertIn('/index', r.headers['Location'])

    def test_login_with_good_credentials_redirects_home(self):
        r = self.client.post('/login', data={
            'email': self.email,
            'password': self.password
        }, follow_redirects=False)
        # success → redirect to /home (protected page) :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}
        self.assertEqual(r.status_code, 302)
        self.assertIn('/home', r.headers['Location'])

    def test_protected_home_requires_login(self):
        r = self.client.get('/home', follow_redirects=False)
        # login_required decorator :contentReference[oaicite:6]{index=6}:contentReference[oaicite:7]{index=7} 
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
        # session cleared → redirect to index :contentReference[oaicite:8]{index=8}:contentReference[oaicite:9]{index=9}
        self.assertEqual(r.status_code, 302)
        self.assertIn('/index', r.headers['Location'])
        # subsequently protected should redirect again
        r2 = self.client.get('/home', follow_redirects=False)
        self.assertEqual(r2.status_code, 302)
