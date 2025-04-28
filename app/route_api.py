from . import app, db, csrf
from flask import request, jsonify, session
import sqlalchemy as sa
from .models import User, Friendship, SharedCalories, CalorieEntry
from sqlalchemy import and_, or_
from datetime import datetime
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
        
        # Get data based on conditions
        query = sa.select(CalorieEntry).where(CalorieEntry.user_id == friend_id)
        
        # Apply condition filters
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
        
        if 'meal_types' in conditions and conditions['meal_types']:
            query = query.where(CalorieEntry.meal_type_id.in_(conditions['meal_types']))
        
        entries = db.session.execute(query).scalars().all()
        
        # Format chart data
        result = []
        for entry in entries:
            result.append({
                'date': entry.date.strftime('%Y-%m-%d'),
                'calories': entry.calories,
                'meal_type_id': entry.meal_type_id,
                'food_detail': entry.food_detail
            })
        
        return json_response({
            'status': 'success',
            'data': result,
            'username': friend.username
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