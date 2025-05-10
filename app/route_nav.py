from . import app, db, csrf
from flask import render_template, flash, session, redirect, url_for, request
import sqlalchemy as sa
from .models import User, Friendship, DailyMetrics, CalorieBurn, ExerciseType, MealType
from sqlalchemy import and_, or_, desc
from .auth import login_required
from datetime import datetime, date
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid, os
from flask import current_app
import json
from flask import jsonify



@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('sharing'))

@app.route('/home')
@login_required
def home():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    days_since = (datetime.utcnow() - user.created_at).days
    return render_template('home.html', title='Home', user=user, days_since=days_since)


@app.route('/upload')
@login_required
def upload():
    user_id = session.get('user_id')
    
    # Fetch recent entries for the current user
    daily_metrics = db.session.execute(
        sa.select(DailyMetrics)
        .where(DailyMetrics.user_id == user_id)
        .order_by(desc(DailyMetrics.date))
        .limit(7)
    ).scalars().all()
    
    calorie_burns = db.session.execute(
        sa.select(CalorieBurn)
        .where(CalorieBurn.user_id == user_id)
        .order_by(desc(CalorieBurn.date), desc(CalorieBurn.created_at))
        .limit(10)
    ).scalars().all()
    
    # Fetch all exercise types
    exercise_types = db.session.execute(
        sa.select(ExerciseType)
        .order_by(ExerciseType.display_name)
    ).scalars().all()
    
    # Fetch all meal types
    meal_types = db.session.execute(
        sa.select(MealType)
        .order_by(MealType.display_name)
    ).scalars().all()
    
    return render_template('upload.html', title='Upload', 
                          daily_metrics=daily_metrics,
                          calorie_burns=calorie_burns,
                          exercise_types=exercise_types,
                          meal_types=meal_types)


@app.route('/visualisation')
@login_required
def visualisation():
    try:
        # Get current user from session
        current_user_id = session.get('user_id')
        user = User.query.get(current_user_id)
        
        # We don't need to pass data directly since JavaScript will fetch it via API
        # But we pass the user object for personalization
        return render_template('visualisation.html', 
                              title='Health Data Insights', 
                              current_user=user)
    except Exception as e:
        print(f"Error in visualization route: {str(e)}")
        flash(f"An error occurred: {str(e)}", "error")
        return render_template('visualisation.html', 
                              title='Health Data Insights',
                              error=str(e))


@app.route('/sharing')
@login_required
def sharing():
    try:
        # Get current user from session
        current_user_id = session.get('user_id')
        
        # Get pending friend requests
        pending_requests = db.session.execute(
            sa.select(Friendship, User)
            .join(User, User.id == Friendship.user_id)
            .where(
                and_(
                    Friendship.friend_id == current_user_id,
                    Friendship.status == 'pending'
                )
            )
        ).all()
        
        # Get friends list
        friends = db.session.execute(
            sa.select(User)
            .join(Friendship, 
                or_(
                    and_(Friendship.user_id == current_user_id, 
                        Friendship.friend_id == User.id),
                    and_(Friendship.friend_id == current_user_id, 
                        Friendship.user_id == User.id)
                ))
            .where(Friendship.status == 'accepted')
            .distinct()
        ).scalars().all()
        
        return render_template('sharing.html', title='Sharing', 
                            pending_requests=pending_requests,
                            friends=friends)
    except Exception as e:
        print(f"Error in sharing route: {str(e)}")
        flash(f"An error occurred: {str(e)}", "error")
        return render_template('sharing.html', title='Sharing',
                             pending_requests=[], friends=[])


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        # Update fields
        user.username = request.form.get('fullName', user.username)
        user.email = request.form.get('email', user.email)
        password = request.form.get('password')
        if password:
            user.password_hash = generate_password_hash(password)
        user.gender = request.form.get('gender', user.gender)
        user.bio = request.form.get('bio', user.bio)
        user.phone = request.form.get('phone', user.phone)
        # Save height and weight
        height = request.form.get('height')
        weight = request.form.get('weight')
        user.height = float(height) if height else None
        user.weight = float(weight) if weight else None
        # Save selected default photo
        selected_photo = request.form.get('photo')
        if selected_photo:
            user.photo = selected_photo
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
        return redirect(url_for('profile'))
    return render_template('profile.html', title='Profile', current_user=user) 


@app.route('/complete-profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.username = request.form.get('fullName', user.username)
        user.email = request.form.get('email', user.email)
        password = request.form.get('password')
        if password:
            user.password_hash = generate_password_hash(password)
        user.gender = request.form.get('gender', user.gender)
        user.bio = request.form.get('bio', user.bio)
        user.phone = request.form.get('phone', user.phone)
        height = request.form.get('height')
        weight = request.form.get('weight')
        user.height = float(height) if height else None
        user.weight = float(weight) if weight else None
        selected_photo = request.form.get('photo')
        if selected_photo:
            user.photo = selected_photo
        try:
            db.session.commit()
            flash('Profile completed successfully!', 'success')
            return redirect(url_for('upload'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving profile: {str(e)}', 'error')
    return render_template('complete_profile.html', title='Complete Profile', current_user=user)

@app.route('/autocomplete')
@login_required
def autocomplete():
    query = request.args.get("query", "").strip().lower()
    json_path = os.path.join(current_app.root_path, 'static', 'data', 'food_basic_nutrition.json')
    with open(json_path) as f:
        food_data = json.load(f)

    results = [
        item["description"]
        for item in food_data
        if query in item["description"].lower()
    ]

    return jsonify(results[:10])  # 返回最多10条
