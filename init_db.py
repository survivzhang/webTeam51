from app import app, db
from app.models import User, MealType, CalorieEntry, Friendship, SharedCalories, ExerciseType, CalorieBurn, DailyMetrics, Food, VerificationCode, Recommendation, UserGoal
from app import models
from werkzeug.security import generate_password_hash
from datetime import datetime
import sqlalchemy as sa
import json
import os

def init_database():
    print("Initializing database...")
    
    with app.app_context():
        try:
            db.create_all()
            print("All tables created successfully!")
            
            # ========== add MealType ==========
            meal_types = [
                MealType(name="breakfast", display_name="Breakfast"),
                MealType(name="lunch", display_name="Lunch"),
                MealType(name="dinner", display_name="Dinner"),
                MealType(name="snacks", display_name="Snacks")
            ]
            for meal_type in meal_types:
                if not db.session.execute(sa.select(MealType).where(MealType.name == meal_type.name)).scalar_one_or_none():
                    db.session.add(meal_type)
            db.session.commit()
            print("Added default meal types")

            # ========== add ExerciseType ==========
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
            for ex_type in exercise_types:
                if not db.session.execute(sa.select(ExerciseType).where(ExerciseType.name == ex_type.name)).scalar_one_or_none():
                    db.session.add(ex_type)
            db.session.commit()
            print("Added default exercise types")

            # ========== add Food data ==========
            food_path = os.path.join(app.root_path, 'static', 'data', 'food_basic_nutrition.json')
            if os.path.exists(food_path):
                with open(food_path, 'r') as f:
                    food_data = json.load(f)

                count = 0
                for item in food_data:
                    if not db.session.execute(sa.select(Food).where(Food.description == item['description'])).scalar_one_or_none():
                        food = Food(
                            description=item['description'],
                            energy_kcal=item.get('energy_kcal', 0),
                            proteins=item.get('protein', 0),
                            fats=item.get('fat', 0),
                            carbohydrates=item.get('carbohydrate', 0),
                            sugars=item.get('sugar', 0),
                            fiber=item.get('fiber', 0)
                        )
                        db.session.add(food)
                        count += 1
                db.session.commit()
                print(f"✅ Imported {count} foods from JSON")
            else:
                print("⚠️ Food JSON file not found")

            # ========== Print data summary ==========
            print("Current database status:")
            print(f"- Users: {db.session.query(User).count()}")
            print(f"- Meal Types: {db.session.query(MealType).count()}")
            print(f"- Exercise Types: {db.session.query(ExerciseType).count()}")
            print(f"- Calorie Entries: {db.session.query(CalorieEntry).count()}")
            print(f"- Calorie Burns: {db.session.query(CalorieBurn).count()}")
            print(f"- Daily Metrics: {db.session.query(DailyMetrics).count()}")
            print(f"- Friendships: {db.session.query(Friendship).count()}")
            print(f"- Shared Calories Settings: {db.session.query(SharedCalories).count()}")
            print(f"- Foods: {db.session.query(Food).count()}")
            print(f"- Verification Codes: {db.session.query(VerificationCode).count()}")
            print(f"- Recommendations: {db.session.query(Recommendation).count()}")
            print(f"- User Goals: {db.session.query(UserGoal).count()}")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            raise

if __name__ == "__main__":
    init_database()
