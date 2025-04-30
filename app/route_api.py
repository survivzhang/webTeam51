from . import app, db, csrf
from flask import request, jsonify, session, redirect, url_for, flash
import sqlalchemy as sa
from .models import User, Friendship, SharedCalories, CalorieEntry, DailyMetrics, CalorieBurn, ExerciseType, MealType
from sqlalchemy import and_, or_, desc
from datetime import datetime, date
import json
from .auth import login_required
from .app_utils import json_response

# Exempt API routes from CSRF
@csrf.exempt
@app.route('/api/friend/request', methods=['POST'])
@login_required
def send_friend_request():
    try:
        # Check if request body is JSON
        if not request.is_json:
            content_type = request.headers.get('Content-Type', 'unknown')
            request_data = request.data.decode('utf-8') if request.data else 'empty'
            print(f"Error: Request is not JSON. Content-Type: {content_type}")
            print(f"Request data: {request_data}")
            return json_response({'status': 'error', 'message': f'Request must be JSON with Content-Type application/json (received: {content_type})'}, 400)
        
        data = request.json
        user_id = session.get('user_id')
        
        print(f"Processing friend request. User ID: {user_id}, Request data: {data}")
        
        # Check if friend_id exists
        if not data or 'friend_id' not in data:
            print(f"Error: Missing friend_id in request data: {data}")
            return json_response({'status': 'error', 'message': 'Missing friend_id parameter'}, 400)
        
        friend_id = data.get('friend_id')
        print(f"Raw friend_id from request: {friend_id}, type: {type(friend_id)}")
        
        # Validate if friend_id is a valid number
        try:
            friend_id = int(friend_id)
        except (ValueError, TypeError):
            print(f"Error: Invalid friend_id: {friend_id}")
            return json_response({'status': 'error', 'message': 'Invalid friend_id parameter: must be an integer'}, 400)
        
        # Check if trying to add self as friend
        if user_id == friend_id:
            print(f"Error: User {user_id} tried to add themselves as friend")
            return json_response({'status': 'error', 'message': 'Cannot add yourself as a friend'}, 400)
            
        # Check if user exists
        friend = db.session.execute(
            sa.select(User).where(User.id == friend_id)
        ).scalar_one_or_none()
        
        if not friend:
            print(f"Error: Friend with ID {friend_id} not found")
            return json_response({'status': 'error', 'message': 'User not found'}, 404)
        
        # Check if already friends or request exists
        existing = db.session.execute(
            sa.select(Friendship)
            .where(
                or_(
                    and_(Friendship.user_id == user_id, Friendship.friend_id == friend_id),
                    and_(Friendship.user_id == friend_id, Friendship.friend_id == user_id)
                )
            )
        ).first()
        
        if existing:
            print(f"Error: Friendship already exists between {user_id} and {friend_id}. Status: {existing[0].status}")
            if existing[0].status == 'pending':
                if existing[0].user_id == user_id:
                    return json_response({'status': 'error', 'message': 'You have already sent a friend request to this user'}, 409)
                else:
                    return json_response({'status': 'error', 'message': 'This user has already sent you a friend request, please check your friend request list'}, 409)
            else:
                return json_response({'status': 'error', 'message': 'You are already friends'}, 409)
        
        # Create new friendship request
        new_request = Friendship(
            user_id=user_id,
            friend_id=friend_id,
            status='pending'
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        print(f"Success: Friend request created from {user_id} to {friend_id} ({friend.username})")
        return json_response({'status': 'success', 'message': f'Friend request sent to {friend.username}'}, 201)
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Error in send_friend_request: {str(e)}")
        print(traceback.format_exc())
        return json_response({'status': 'error', 'message': f'Error processing request: {str(e)}'}, 500)


@csrf.exempt
@app.route('/api/friend/respond', methods=['POST'])
@login_required
def respond_to_request():
    try:
        # Check if request body is JSON
        if not request.is_json:
            print(f"Error: Request is not JSON. Content-Type: {request.headers.get('Content-Type')}")
            print(f"Request data: {request.data}")
            return json_response({'status': 'error', 'message': 'Request must be JSON with Content-Type application/json'}, 400)
            
        data = request.json
        request_id = data.get('request_id')
        action = data.get('action')  # 'accept' or 'decline'
        
        if not request_id or not action:
            return json_response({'status': 'error', 'message': 'Missing request_id or action parameter'}, 400)
        
        try:
            request_id = int(request_id)
        except (ValueError, TypeError):
            return json_response({'status': 'error', 'message': 'Invalid request_id parameter'}, 400)
            
        friend_request = db.session.get(Friendship, request_id)
        
        if not friend_request:
            return json_response({'status': 'error', 'message': 'Request not found'}, 404)
        
        if action == 'accept':
            friend_request.status = 'accepted'
            db.session.commit()
            return json_response({'status': 'success', 'message': 'Friend request accepted'})
        elif action == 'decline':
            db.session.delete(friend_request)
            db.session.commit()
            return json_response({'status': 'success', 'message': 'Friend request declined'})
        
        return json_response({'status': 'error', 'message': 'Invalid action'}, 400)
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Error in respond_to_request: {str(e)}")
        print(traceback.format_exc())
        return json_response({'status': 'error', 'message': f'Error processing request: {str(e)}'}, 500)


@csrf.exempt
@app.route('/api/friend/data/<int:friend_id>', methods=['GET'])
@login_required
def get_friend_data(friend_id):
    try:
        user_id = session.get('user_id')
        
        # Check if ID is valid
        if not friend_id:
            return json_response({'status': 'error', 'message': 'Invalid friend ID'}, 400)
            
        # Check if friendship exists
        friendship = db.session.execute(
            sa.select(Friendship, User)
            .join(User, User.id == Friendship.user_id)
            .where(
                or_(
                    and_(Friendship.user_id == user_id, Friendship.friend_id == friend_id, Friendship.status == 'accepted'),
                    and_(Friendship.user_id == friend_id, Friendship.friend_id == user_id, Friendship.status == 'accepted')
                )
            )
        ).first()
        
        if not friendship:
            return json_response({'status': 'error', 'message': 'You are not friends with this user'}, 403)
        
        # Get friend's username
        friend = db.session.execute(
            sa.select(User).where(User.id == friend_id)
        ).scalar_one_or_none()
        
        if not friend:
            return json_response({'status': 'error', 'message': 'User not found'}, 404)
        
        # Get sharing settings conditions
        shared_settings = db.session.execute(
            sa.select(SharedCalories)
            .where(
                and_(
                    SharedCalories.sharer_id == friend_id,
                    SharedCalories.recipient_id == user_id
                )
            )
        ).scalars().first()
        
        if not shared_settings:
            return json_response({'status': 'error', 'message': 'This user has not shared data with you'}, 404)
        
        # Parse JSON conditions
        try:
            conditions = json.loads(shared_settings.conditions)
        except json.JSONDecodeError:
            return json_response({'status': 'error', 'message': 'Error parsing sharing settings'}, 500)
        
        result = []

        # Get calorie entries based on conditions if meal_types are shared
        if 'meal_types' in conditions and conditions['meal_types']:
            query = sa.select(CalorieEntry).join(MealType).where(CalorieEntry.user_id == friend_id)
            
            # Apply date filters
            if 'date_from' in conditions and conditions['date_from']:
                try:
                    date_from = datetime.strptime(conditions['date_from'], '%Y-%m-%d').date()
                    query = query.where(CalorieEntry.date >= date_from)
                except Exception as e:
                    print(f"Error parsing date_from: {e}")
            
            if 'date_to' in conditions and conditions['date_to']:
                try:
                    date_to = datetime.strptime(conditions['date_to'], '%Y-%m-%d').date()
                    query = query.where(CalorieEntry.date <= date_to)
                except Exception as e:
                    print(f"Error parsing date_to: {e}")
            
            # Apply meal type filter
            query = query.where(CalorieEntry.meal_type_id.in_(conditions['meal_types']))
            
            entries = db.session.execute(query).scalars().all()
            
            # Format meal data
            for entry in entries:
                result.append({
                    'date': entry.date.strftime('%Y-%m-%d'),
                    'type': 'meal',
                    'value': entry.calories,
                    'meal_type': entry.meal_type.display_name,
                    'calories': entry.calories
                })
        
        # Get exercise data if exercise_types are shared
        if 'exercise_types' in conditions and conditions['exercise_types']:
            query = sa.select(CalorieBurn).join(ExerciseType).where(CalorieBurn.user_id == friend_id)
            
            # Apply date filters
            if 'date_from' in conditions and conditions['date_from']:
                try:
                    date_from = datetime.strptime(conditions['date_from'], '%Y-%m-%d').date()
                    query = query.where(CalorieBurn.date >= date_from)
                except Exception as e:
                    print(f"Error parsing date_from: {e}")
            
            if 'date_to' in conditions and conditions['date_to']:
                try:
                    date_to = datetime.strptime(conditions['date_to'], '%Y-%m-%d').date()
                    query = query.where(CalorieBurn.date <= date_to)
                except Exception as e:
                    print(f"Error parsing date_to: {e}")
            
            # Apply exercise type filter
            query = query.where(ExerciseType.name.in_(conditions['exercise_types']))
            
            burns = db.session.execute(query).scalars().all()
            
            # Format exercise data
            for burn in burns:
                result.append({
                    'date': burn.date.strftime('%Y-%m-%d'),
                    'type': 'exercise',
                    'value': burn.calories_burned or 0,
                    'exercise_type': burn.exercise_type.display_name,
                    'duration': burn.duration,
                    'calories_burned': burn.calories_burned
                })
        
        # Get daily metrics if shared
        if 'daily_metrics' in conditions and conditions['daily_metrics']:
            query = sa.select(DailyMetrics).where(DailyMetrics.user_id == friend_id)
            
            # Apply date filters
            if 'date_from' in conditions and conditions['date_from']:
                try:
                    date_from = datetime.strptime(conditions['date_from'], '%Y-%m-%d').date()
                    query = query.where(DailyMetrics.date >= date_from)
                except Exception as e:
                    print(f"Error parsing date_from: {e}")
            
            if 'date_to' in conditions and conditions['date_to']:
                try:
                    date_to = datetime.strptime(conditions['date_to'], '%Y-%m-%d').date()
                    query = query.where(DailyMetrics.date <= date_to)
                except Exception as e:
                    print(f"Error parsing date_to: {e}")
            
            metrics = db.session.execute(query).scalars().all()
            
            # Filter out metrics that aren't shared
            for metric in metrics:
                metric_data = {}
                metric_data['date'] = metric.date.strftime('%Y-%m-%d')
                metric_data['type'] = 'metrics'
                
                # Add value based on which metric type is being shown
                if 'weight' in conditions['daily_metrics'] and metric.weight:
                    metric_data['weight'] = metric.weight
                    metric_data['value'] = metric.weight
                elif 'sleep' in conditions['daily_metrics'] and metric.sleep_hours:
                    metric_data['sleep_hours'] = metric.sleep_hours
                    metric_data['value'] = metric.sleep_hours
                elif 'mood' in conditions['daily_metrics'] and metric.mood:
                    metric_data['mood'] = metric.mood
                    metric_data['value'] = 0  # Mood doesn't have a numeric value
                
                # Only add if at least one metric is shared
                if len(metric_data) > 3:  # date, type and value are always included
                    result.append(metric_data)
        
        # Sort all data by date (descending)
        result.sort(key=lambda x: x['date'], reverse=True)
        
        return json_response({
            'status': 'success',
            'data': result,
            'username': friend.username,
            'sharing_conditions': conditions
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_friend_data: {str(e)}")
        print(traceback.format_exc())
        return json_response({'status': 'error', 'message': f'Error retrieving data: {str(e)}'}, 500)


@csrf.exempt
@app.route('/api/share/settings', methods=['POST'])
@login_required
def update_share_settings():
    try:
        # Check if request body is JSON
        if not request.is_json:
            print(f"Error: Request is not JSON. Content-Type: {request.headers.get('Content-Type')}")
            print(f"Request data: {request.data}")
            return json_response({'status': 'error', 'message': 'Request must be JSON with Content-Type application/json'}, 400)
            
        data = request.json
        user_id = session.get('user_id')
        recipient_id = data.get('recipient_id')
        conditions = data.get('conditions', {})
        
        if not recipient_id:
            return json_response({'status': 'error', 'message': 'Recipient ID cannot be empty'}, 400)
            
        # Check if recipient exists
        recipient = db.session.execute(
            sa.select(User).where(User.id == recipient_id)
        ).scalar_one_or_none()
        
        if not recipient:
            return json_response({'status': 'error', 'message': 'Recipient user not found'}, 404)
            
        # Check if friendship exists
        friendship = db.session.execute(
            sa.select(Friendship)
            .where(
                or_(
                    and_(Friendship.user_id == user_id, Friendship.friend_id == recipient_id, Friendship.status == 'accepted'),
                    and_(Friendship.user_id == recipient_id, Friendship.friend_id == user_id, Friendship.status == 'accepted')
                )
            )
        ).first()
        
        if not friendship:
            return json_response({'status': 'error', 'message': 'You are not friends with this user'}, 403)
        
        # Ensure dates are valid or set to None
        if 'date_from' in conditions and not conditions['date_from']:
            conditions['date_from'] = None
            
        if 'date_to' in conditions and not conditions['date_to']:
            conditions['date_to'] = None
            
        # Ensure meal_types is a list
        if 'meal_types' not in conditions or not isinstance(conditions['meal_types'], list):
            conditions['meal_types'] = []
            
        # Ensure exercise_types is a list
        if 'exercise_types' not in conditions or not isinstance(conditions['exercise_types'], list):
            conditions['exercise_types'] = []
            
        # Ensure daily_metrics is a list
        if 'daily_metrics' not in conditions or not isinstance(conditions['daily_metrics'], list):
            conditions['daily_metrics'] = []
        
        # Check if sharing settings already exist
        existing = db.session.execute(
            sa.select(SharedCalories)
            .where(
                and_(
                    SharedCalories.sharer_id == user_id,
                    SharedCalories.recipient_id == recipient_id
                )
            )
        ).scalars().first()
        
        if existing:
            # Update existing settings
            existing.conditions = json.dumps(conditions)
        else:
            # Create new settings
            new_settings = SharedCalories(
                sharer_id=user_id,
                recipient_id=recipient_id,
                conditions=json.dumps(conditions)
            )
            db.session.add(new_settings)
        
        db.session.commit()
        return json_response({'status': 'success', 'message': 'Sharing settings saved'})
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Error in update_share_settings: {str(e)}")
        print(traceback.format_exc())
        return json_response({'status': 'error', 'message': f'Error saving settings: {str(e)}'}, 500)


@csrf.exempt
@app.route('/api/users/search', methods=['GET'])
@login_required
def search_users():
    try:
        query = request.args.get('q', '')
        user_id = session.get('user_id')
        
        if not query or len(query) < 2:
            return json_response({'users': []})
        
        users = db.session.execute(
            sa.select(User)
            .where(
                and_(
                    User.username.like(f'%{query}%'),
                    User.id != user_id
                )
            )
            .limit(10)
        ).scalars().all()
        
        result = [{'id': user.id, 'username': user.username} for user in users]
        return json_response({'users': result})
    except Exception as e:
        import traceback
        print(f"Error in search_users: {str(e)}")
        print(traceback.format_exc())
        return json_response({'users': [], 'error': str(e)})


@csrf.exempt
@app.route('/api/save_daily_metrics', methods=['POST'])
@login_required
def save_daily_metrics():
    user_id = session.get('user_id')
    today = date.today()
    
    # Get form data
    weight = request.form.get('weight', type=float)
    sleep_hours = request.form.get('sleep_hours', type=float)
    mood = request.form.get('mood')
    
    # Check if at least one field is filled
    if not any([weight, sleep_hours, mood]):
        flash('Please fill in at least one field', 'error')
        return redirect(url_for('upload'))
    
    try:
        # Check if entry already exists for today
        existing_entry = db.session.execute(
            sa.select(DailyMetrics)
            .where(and_(DailyMetrics.user_id == user_id, DailyMetrics.date == today))
        ).scalar_one_or_none()
        
        if existing_entry:
            # Update existing entry
            if weight is not None:
                existing_entry.weight = weight
            if sleep_hours is not None:
                existing_entry.sleep_hours = sleep_hours
            if mood:
                existing_entry.mood = mood
        else:
            # Create new entry
            new_entry = DailyMetrics(
                user_id=user_id,
                date=today,
                weight=weight,
                sleep_hours=sleep_hours,
                mood=mood
            )
            db.session.add(new_entry)
        
        db.session.commit()
        flash('Daily metrics updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving daily metrics: {str(e)}', 'error')
    
    return redirect(url_for('upload'))


@csrf.exempt
@app.route('/api/save_exercise', methods=['POST'])
@login_required
def save_exercise():
    user_id = session.get('user_id')
    today = date.today()
    
    # Get form data
    exercise_type_id = request.form.get('exercise_type_id', type=int)
    duration = request.form.get('duration', type=int)
    calories_burned = request.form.get('calories_burned', type=int)
    
    # Validate required fields
    if not exercise_type_id or not duration:
        flash('Please select an exercise type and enter duration', 'error')
        return redirect(url_for('upload'))
    
    try:
        # Verify exercise type exists
        exercise_type = db.session.get(ExerciseType, exercise_type_id)
        if not exercise_type:
            flash('Invalid exercise type', 'error')
            return redirect(url_for('upload'))
        
        # Create new calorie burn entry
        new_burn = CalorieBurn(
            user_id=user_id,
            date=today,
            exercise_type_id=exercise_type_id,
            duration=duration,
            calories_burned=calories_burned
        )
        
        db.session.add(new_burn)
        db.session.commit()
        flash('Exercise added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving exercise: {str(e)}', 'error')
    
    return redirect(url_for('upload'))


@csrf.exempt
@app.route('/api/user/data_options', methods=['GET'])
@login_required
def get_user_data_options():
    user_id = session.get('user_id')
    
    try:
        # exercise types
        exercise_types = db.session.execute(
            sa.select(ExerciseType.id, ExerciseType.display_name)
            .distinct()
        ).all()
        
        exercise_type_options = [{'id': et.id, 'name': et.display_name} for et in exercise_types]
        
        # meal types
        meal_types = db.session.execute(
            sa.select(CalorieEntry.meal_type_id)
            .where(CalorieEntry.user_id == user_id)
            .distinct()
        ).scalars().all()
        
        # date_range
        date_range = db.session.execute(
            sa.select(
                sa.func.min(DailyMetrics.date),
                sa.func.max(DailyMetrics.date)
            )
            .where(DailyMetrics.user_id == user_id)
        ).first()
        
        min_date = date_range[0].strftime('%Y-%m-%d') if date_range[0] else None
        max_date = date_range[1].strftime('%Y-%m-%d') if date_range[1] else None
        
        return json_response({
            'status': 'success',
            'data': {
                'exercise_types': exercise_type_options,
                'meal_types': meal_types,
                'date_range': {
                    'min': min_date,
                    'max': max_date
                }
            }
        })
    except Exception as e:
        import traceback
        print(f"Error in get_user_data_options: {str(e)}")
        print(traceback.format_exc())
        return json_response({'status': 'error', 'message': f'Error retrieving data options: {str(e)}'}, 500)


@csrf.exempt
@app.route('/api/save_meal', methods=['POST'])
@login_required
def save_meal():
    user_id = session.get('user_id')
    today = date.today()
    
    # Get form data
    meal_type_id = request.form.get('meal_type_id', type=int)
    calories = request.form.get('calories', type=int)
    
    # Validate required fields
    if not meal_type_id or not calories:
        flash('Please select a meal type and enter calories', 'error')
        return redirect(url_for('upload'))
    
    try:
        # Verify meal type exists
        meal_type = db.session.get(MealType, meal_type_id)
        if not meal_type:
            flash('Invalid meal type', 'error')
            return redirect(url_for('upload'))
        
        # Create new calorie entry
        new_entry = CalorieEntry(
            user_id=user_id,
            date=today,
            meal_type_id=meal_type_id,
            calories=calories
        )
        
        db.session.add(new_entry)
        db.session.commit()
        flash('Meal added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving meal: {str(e)}', 'error')
    
    return redirect(url_for('upload'))


@csrf.exempt
@app.route('/api/get_all_data', methods=['GET'])
@login_required
def get_all_data():
    user_id = session.get('user_id')
    
    try:
        # Get calorie entries
        calorie_entries = db.session.execute(
            sa.select(CalorieEntry).join(MealType)
            .where(CalorieEntry.user_id == user_id)
            .order_by(desc(CalorieEntry.date))
        ).scalars().all()
        
        # Get calorie burns
        calorie_burns = db.session.execute(
            sa.select(CalorieBurn).join(ExerciseType)
            .where(CalorieBurn.user_id == user_id)
            .order_by(desc(CalorieBurn.date))
        ).scalars().all()
        
        # Format data
        entries = []
        for entry in calorie_entries:
            entries.append({
                'type': 'meal',
                'date': entry.date.strftime('%Y-%m-%d'),
                'meal_type': entry.meal_type.display_name,
                'calories': entry.calories
            })
            
        for burn in calorie_burns:
            entries.append({
                'type': 'exercise',
                'date': burn.date.strftime('%Y-%m-%d'),
                'exercise_type': burn.exercise_type.display_name,
                'duration': burn.duration,
                'calories_burned': burn.calories_burned
            })
            
        # Sort by date descending
        entries.sort(key=lambda x: x['date'], reverse=True)
        
        return json_response({
            'status': 'success',
            'data': entries
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_all_data: {str(e)}")
        print(traceback.format_exc())
        return json_response({'status': 'error', 'message': f'Error retrieving data: {str(e)}'}, 500)