from . import app, db, csrf
from flask import render_template, flash, session, redirect, url_for, request
import sqlalchemy as sa
from .models import User, Friendship, DailyMetrics, CalorieBurn, ExerciseType, MealType
from sqlalchemy import and_, or_, desc
from .auth import login_required
from datetime import datetime, date


@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('sharing'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='Home')


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
    return render_template('visualisation.html', title='Visualisation')


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


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile') 