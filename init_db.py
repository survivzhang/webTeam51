from app import app, db
from app.models import User, MealType, CalorieEntry, Friendship, SharedCalories
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
            
            # Create initial users
            admin = User(
                username='admin@example.com',
                password_hash=generate_password_hash('root'),
                created_at=datetime.utcnow()
            )
            db.session.add(admin)

            guests = [
                User(username='guest1@example.com', password_hash=generate_password_hash('guest1'), created_at=datetime.utcnow()),
                User(username='guest2@example.com', password_hash=generate_password_hash('guest2'), created_at=datetime.utcnow()),
                User(username='guest3@example.com', password_hash=generate_password_hash('guest3'), created_at=datetime.utcnow()),
                User(username='guest4@example.com', password_hash=generate_password_hash('guest4'), created_at=datetime.utcnow())
            ]
            db.session.add_all(guests)
            
            # Create meal types
            meal_types = [
                MealType(name="breakfast", display_name="Breakfast"),
                MealType(name="lunch", display_name="Lunch"),
                MealType(name="dinner", display_name="Dinner"),
                MealType(name="snacks", display_name="Snacks")
            ]
            
            # Add meal types
            db.session.add_all(meal_types)
            
            # Commit all changes
            db.session.commit()
            print("Added default users and meal types")
            
            # Check database status
            user_count = db.session.query(User).count()
            meal_type_count = db.session.query(MealType).count()
            entry_count = db.session.query(CalorieEntry).count()
            friendship_count = db.session.query(Friendship).count()
            shared_count = db.session.query(SharedCalories).count()
            
            print(f"Current database status:")
            print(f"- Users: {user_count}")
            print(f"- Meal Types: {meal_type_count}")
            print(f"- Calorie Entries: {entry_count}")
            print(f"- Friendships: {friendship_count}")
            print(f"- Shared Calories Settings: {shared_count}")
            
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            raise

if __name__ == "__main__":
    init_database() 