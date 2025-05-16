import unittest
from werkzeug.security import generate_password_hash
import sys
import os
from sqlalchemy import inspect
from datetime import date
import json

# Add parent directory to path to import app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, CalorieEntry, CalorieBurn, MealType, ExerciseType, Friendship, SharedCalories
from config import TestingConfig
from flask import session

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
        self.assertTrue(inspect(db.engine).has_table('users'))
            
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


class CalorieTrackingTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Test client
        self.client = self.app.test_client()
        
        # Create tables and seed test data
        db.create_all()
        
        # Add meal types
        breakfast = MealType(name='breakfast', display_name='Breakfast')
        lunch = MealType(name='lunch', display_name='Lunch')
        dinner = MealType(name='dinner', display_name='Dinner')
        db.session.add_all([breakfast, lunch, dinner])
        
        # Add exercise types
        running = ExerciseType(name='running', display_name='Running')
        cycling = ExerciseType(name='cycling', display_name='Cycling')
        db.session.add_all([running, cycling])
        
        # Create test user
        self.user = User(
            username='caltracker',
            email='caltrack@example.com',
            password_hash=generate_password_hash('TestPass123'),
            height=180.0,
            weight=75.0
        )
        db.session.add(self.user)
        db.session.commit()
        
        # Store IDs for testing
        self.user_id = self.user.id
        self.breakfast_id = breakfast.id
        self.running_id = running.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def login(self):
        """Helper method to log in the test user"""
        return self.client.post('/login', data={
            'email': 'caltrack@example.com',
            'password': 'TestPass123'
        }, follow_redirects=True)
    
    def test_add_meal(self):
        """Test adding a meal entry"""
        # Login first
        self.login()
        
        # Add a meal entry
        response = self.client.post('/api/save_meal', data={
            'meal_type_id': self.breakfast_id,
            'total_calories': 500,
            'total_proteins': 20,
            'total_fats': 15,
            'total_carbohydrates': 60,
            'total_fiber': 5,
            'total_sugars': 10
        }, follow_redirects=True)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        
        # Verify entry was added to database
        entry = CalorieEntry.query.filter_by(user_id=self.user_id).first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.meal_type_id, self.breakfast_id)
        self.assertEqual(entry.calories, 500)
        self.assertEqual(entry.proteins, 20)
        self.assertEqual(entry.date, date.today())
    
    def test_add_exercise(self):
        """Test adding an exercise entry"""
        # Login first
        self.login()
        
        # Add an exercise entry
        response = self.client.post('/api/save_exercise', data={
            'exercise_type_id': self.running_id,
            'duration': 30,
            'calories_burned': 300
        }, follow_redirects=True)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        
        # Verify entry was added to database
        entry = CalorieBurn.query.filter_by(user_id=self.user_id).first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.exercise_type_id, self.running_id)
        self.assertEqual(entry.duration, 30)
        self.assertEqual(entry.calories_burned, 300)
        self.assertEqual(entry.date, date.today())
    
    def test_get_all_data(self):
        """Test retrieving all calorie data"""
        # Login first
        self.login()
        
        # Add test data
        meal = CalorieEntry(
            user_id=self.user_id,
            meal_type_id=self.breakfast_id,
            date=date.today(),
            calories=400,
            proteins=15,
            fats=12,
            carbohydrates=50,
            fiber=3,
            sugars=8
        )
        
        exercise = CalorieBurn(
            user_id=self.user_id,
            exercise_type_id=self.running_id,
            date=date.today(),
            duration=45,
            calories_burned=450
        )
        
        db.session.add_all([meal, exercise])
        db.session.commit()
        
        # Get all data
        response = self.client.get('/api/get_all_data')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 2)  # Should have both entries
        
        # Check for both types of entries
        entry_types = [entry['type'] for entry in data['data']]
        self.assertIn('meal', entry_types)
        self.assertIn('exercise', entry_types)


class FriendshipTests(unittest.TestCase):
    def setUp(self):
        """Set up test environment for friendship tests"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Test client
        self.client = self.app.test_client()
        
        # Create tables
        db.create_all()
        
        # Create main test user
        self.user1 = User(
            username='user1',
            email='user1@example.com',
            password_hash=generate_password_hash('Password123'),
            is_verified=True
        )
        
        # Create potential friend user
        self.user2 = User(
            username='user2',
            email='user2@example.com',
            password_hash=generate_password_hash('Password123'),
            is_verified=True
        )
        
        db.session.add_all([self.user1, self.user2])
        db.session.commit()
        
        # Store user IDs
        self.user1_id = self.user1.id
        self.user2_id = self.user2.id

    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def login_user1(self):
        """Helper to log in as user1"""
        return self.client.post('/login', data={
            'email': 'user1@example.com',
            'password': 'Password123'
        }, follow_redirects=True)
    
    def test_send_friend_request(self):
        """Test sending a friend request"""
        # Log in first
        self.login_user1()
        
        # Send friend request
        response = self.client.post('/api/send_friend_request', json={
            'friend_username': 'user2'
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        
        # Verify friendship was created in database with 'pending' status
        friendship = Friendship.query.filter_by(
            user_id=self.user1_id, 
            friend_id=self.user2_id
        ).first()
        
        self.assertIsNotNone(friendship)
        self.assertEqual(friendship.status, 'pending')
    
    def test_accept_friend_request(self):
        """Test accepting a friend request"""
        # Create a pending friendship first
        friendship = Friendship(
            user_id=self.user2_id,
            friend_id=self.user1_id,
            status='pending'
        )
        db.session.add(friendship)
        db.session.commit()
        
        # Log in as user1 to accept request
        self.login_user1()
        
        # Accept the request
        response = self.client.post('/api/respond_to_friend_request', json={
            'request_id': friendship.id,
            'action': 'accept'
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        
        # Verify friendship status was updated to 'accepted'
        updated_friendship = Friendship.query.get(friendship.id)
        self.assertEqual(updated_friendship.status, 'accepted')
    
    def test_decline_friend_request(self):
        """Test declining a friend request"""
        # Create a pending friendship first
        friendship = Friendship(
            user_id=self.user2_id,
            friend_id=self.user1_id,
            status='pending'
        )
        db.session.add(friendship)
        db.session.commit()
        
        # Log in as user1 to decline request
        self.login_user1()
        
        # Decline the request
        response = self.client.post('/api/respond_to_friend_request', json={
            'request_id': friendship.id,
            'action': 'decline'
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        
        # Verify friendship was removed from database
        friendship = Friendship.query.get(friendship.id)
        self.assertIsNone(friendship)


class DataSharingTests(unittest.TestCase):
    def setUp(self):
        """Set up test environment for data sharing tests"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Test client
        self.client = self.app.test_client()
        
        # Create tables
        db.create_all()
        
        # Create main test user (sharer)
        self.sharer = User(
            username='sharer',
            email='sharer@example.com',
            password_hash=generate_password_hash('Password123'),
            is_verified=True
        )
        
        # Create recipient user
        self.recipient = User(
            username='recipient',
            email='recipient@example.com',
            password_hash=generate_password_hash('Password123'),
            is_verified=True
        )
        
        # Create accepted friendship
        db.session.add_all([self.sharer, self.recipient])
        db.session.commit()
        
        # Store user IDs
        self.sharer_id = self.sharer.id
        self.recipient_id = self.recipient.id
        
        # Create friendship connection (accepted)
        friendship = Friendship(
            user_id=self.sharer_id,
            friend_id=self.recipient_id,
            status='accepted'
        )
        db.session.add(friendship)
        db.session.commit()

    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def login_sharer(self):
        """Helper to log in as sharer"""
        return self.client.post('/login', data={
            'email': 'sharer@example.com',
            'password': 'Password123'
        }, follow_redirects=True)
    
    def login_recipient(self):
        """Helper to log in as recipient"""
        return self.client.post('/login', data={
            'email': 'recipient@example.com',
            'password': 'Password123'
        }, follow_redirects=True)
    
    def test_create_sharing_settings(self):
        """Test creating data sharing settings with a friend"""
        # Log in as sharer
        self.login_sharer()
        
        # Define sharing conditions
        conditions = {
            'meal_types': [1, 2],  # breakfast and lunch
            'exercise_types': ['running', 'walking']
        }
        
        # Create sharing settings
        response = self.client.post('/api/set_sharing_settings', json={
            'recipient_id': self.recipient_id,
            'conditions': conditions
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        
        # Verify settings were saved in database
        sharing = SharedCalories.query.filter_by(
            sharer_id=self.sharer_id,
            recipient_id=self.recipient_id
        ).first()
        
        self.assertIsNotNone(sharing)
        saved_conditions = json.loads(sharing.conditions)
        self.assertEqual(saved_conditions['meal_types'], conditions['meal_types'])
        self.assertEqual(saved_conditions['exercise_types'], conditions['exercise_types'])
    
    def test_update_sharing_settings(self):
        """Test updating existing sharing settings"""
        # Create initial sharing settings
        initial_conditions = json.dumps({
            'meal_types': [1],
            'exercise_types': ['running']
        })
        
        sharing = SharedCalories(
            sharer_id=self.sharer_id,
            recipient_id=self.recipient_id,
            conditions=initial_conditions
        )
        db.session.add(sharing)
        db.session.commit()
        
        # Log in as sharer
        self.login_sharer()
        
        # Updated conditions
        new_conditions = {
            'meal_types': [1, 2, 3],  # breakfast, lunch, dinner
            'exercise_types': ['cycling', 'swimming']
        }
        
        # Update sharing settings
        response = self.client.post('/api/set_sharing_settings', json={
            'recipient_id': self.recipient_id,
            'conditions': new_conditions
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        
        # Verify settings were updated
        updated_sharing = SharedCalories.query.get(sharing.id)
        updated_conditions = json.loads(updated_sharing.conditions)
        self.assertEqual(updated_conditions['meal_types'], new_conditions['meal_types'])
        self.assertEqual(updated_conditions['exercise_types'], new_conditions['exercise_types'])
    
    def test_view_shared_data(self):
        """Test viewing shared data from a friend"""
        # Create sharing settings
        conditions = json.dumps({
            'meal_types': [1, 2],  # breakfast and lunch
            'exercise_types': ['running', 'walking']
        })
        
        sharing = SharedCalories(
            sharer_id=self.sharer_id,
            recipient_id=self.recipient_id,
            conditions=conditions
        )
        db.session.add(sharing)
        db.session.commit()
        
        # Log in as recipient
        self.login_recipient()
        
        # Request shared data
        response = self.client.get(f'/api/get_friend_data/{self.sharer_id}')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        
        # Verify shared settings are returned
        self.assertIn('sharing_settings', data)
        self.assertEqual(data['friend_id'], self.sharer_id)
