import unittest
import sys
import os
from datetime import date

# Add parent directory to path to import app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, CalorieEntry, CalorieBurn, MealType, ExerciseType
from config import TestingConfig
from werkzeug.security import generate_password_hash
from flask import session

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

if __name__ == "__main__":
    unittest.main() 