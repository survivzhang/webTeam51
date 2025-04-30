from app import app, db
from app.models import User, MealType, CalorieEntry, Friendship, SharedCalories, ExerciseType, CalorieBurn, DailyMetrics
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Initialize the database by creating all tables"""
    print("Initializing database...")
    
    with app.app_context():
        # Create all tables
        try:
            db.create_all()
            print("All tables created successfully!")
            
            # Create meal types
            meal_types = [
                MealType(name="breakfast", display_name="Breakfast"),
                MealType(name="lunch", display_name="Lunch"),
                MealType(name="dinner", display_name="Dinner"),
                MealType(name="snacks", display_name="Snacks")
            ]
            # Add meal types
            db.session.add_all(meal_types)
            print("Added default meal types")
            
            # Create exercise types
            exercise_types = [
                ExerciseType(name="running", display_name="Running"),
                ExerciseType(name="swimming", display_name="Swimming"),
                ExerciseType(name="cycling", display_name="Cycling"),
                ExerciseType(name="weightlifting", display_name="Weightlifting"),
                ExerciseType(name="yoga", display_name="Yoga"),
                ExerciseType(name="walking", display_name="Walking"),
                ExerciseType(name="hiit", display_name="HIIT"),
                ExerciseType(name="pilates", display_name="Pilates")
            ]
            
            # Add exercise types
            db.session.add_all(exercise_types)
            print("Added default exercise types")
            
            # Commit all changes
            db.session.commit()
            
            # Check database status
            user_count = db.session.query(User).count()
            meal_type_count = db.session.query(MealType).count()
            exercise_type_count = db.session.query(ExerciseType).count()
            entry_count = db.session.query(CalorieEntry).count()
            burn_count = db.session.query(CalorieBurn).count()
            friendship_count = db.session.query(Friendship).count()
            shared_count = db.session.query(SharedCalories).count()
            metrics_count = db.session.query(DailyMetrics).count()
            
            print(f"Current database status:")
            print(f"- Users: {user_count}")
            print(f"- Meal Types: {meal_type_count}")
            print(f"- Exercise Types: {exercise_type_count}")
            print(f"- Calorie Entries: {entry_count}")
            print(f"- Calorie Burns: {burn_count}")
            print(f"- Daily Metrics: {metrics_count}")
            print(f"- Friendships: {friendship_count}")
            print(f"- Shared Calories Settings: {shared_count}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating tables: {str(e)}")
            raise

if __name__ == "__main__":
    init_database() 