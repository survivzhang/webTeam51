from flask import render_template, flash, session, redirect, url_for, request
import sqlalchemy as sa
from .models import User, Friendship, DailyMetrics, CalorieBurn, ExerciseType, MealType, CalorieEntry, UserGoal
from sqlalchemy import and_, or_, desc
from .auth import login_required
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid, os
from flask import current_app, jsonify
import json
from . import db, csrf
from .blueprints import main


@main.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('main.sharing'))

@main.route('/home')
@login_required
def home():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    now = datetime.utcnow()
    days_since = (now.date() - user.created_at.date()).days

    # Get unique dates from both calorie entries and burns, ordered by most recent first
    calorie_dates = db.session.query(CalorieEntry.date).filter(
        CalorieEntry.user_id == user_id
    ).distinct().order_by(desc(CalorieEntry.date)).limit(7).all()
    
    burn_dates = db.session.query(CalorieBurn.date).filter(
        CalorieBurn.user_id == user_id
    ).distinct().order_by(desc(CalorieBurn.date)).limit(7).all()
    
    # Combine and get unique dates
    unique_dates = list(set([date[0] for date in calorie_dates + burn_dates]))
    unique_dates.sort(reverse=True)  # Most recent first
    
    # Take up to 7 most recent dates
    recent_dates = unique_dates[:7]
    
    # If no entries exist, use the current date and 6 days before
    if not recent_dates:
        start_date = now.date() - timedelta(days=6)
        recent_dates = [(start_date + timedelta(days=i)) for i in range(7)]
        recent_dates.sort(reverse=True)  # Most recent first
    
    # Create a dictionary to track entries by date
    entries_by_date = {}
    
    # Process each date to get calories in and out
    for entry_date in recent_dates:
        date_str = entry_date.strftime('%b %d')
        
        # Get calories in for this date
        calories_in = db.session.query(sa.func.sum(CalorieEntry.calories)).filter(
            CalorieEntry.user_id == user_id,
            CalorieEntry.date == entry_date
        ).scalar() or 0
        
        # Get calories out for this date
        calories_out = db.session.query(sa.func.sum(CalorieBurn.calories_burned)).filter(
            CalorieBurn.user_id == user_id,
            CalorieBurn.date == entry_date
        ).scalar() or 0
        
        entries_by_date[date_str] = {
            'in': round(calories_in),
            'out': round(calories_out)
        }
    
    # Sort dates chronologically from oldest to newest (left to right on chart)
    recent_dates.sort()  # Sort dates in ascending order
    
    # Convert dates to formatted strings for chart labels
    sorted_dates = [date.strftime('%b %d') for date in recent_dates]
    
    # Prepare data for the chart
    labels = sorted_dates
    calories_in = [entries_by_date[date]['in'] for date in labels]
    calories_out = [entries_by_date[date]['out'] for date in labels]

    return render_template(
        'home.html',
        title='Home',
        user=user,
        days_since=days_since,
        data_labels=labels,
        calories_in=calories_in,
        calories_out=calories_out
    )


@main.route('/upload')
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


@main.route('/visualisation')
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


@main.route('/sharing')
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


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    goal = UserGoal.query.filter_by(user_id=user.id).first()
    if not goal:
        # Create a goal record if not exists, using current profile values
        goal = UserGoal(user_id=user.id, initial_weight=user.weight or 0, target_weight=user.target_weight, current_weight=user.weight or 0)
        db.session.add(goal)
        db.session.commit()

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
        height = request.form.get('height')
        user.height = float(height) if height else None
        # Save selected default photo
        selected_photo = request.form.get('photo')
        if selected_photo:
            user.photo = selected_photo
        # Weight logic
        new_weight = request.form.get('weight')
        new_target_weight = request.form.get('target_weight')
        reset_initial = request.form.get('reset_initial_weight') == '1'
        # Update current weight
        if new_weight:
            user.weight = float(new_weight)
            goal.current_weight = float(new_weight)
        # Update target weight
        if new_target_weight:
            user.target_weight = float(new_target_weight)
            goal.target_weight = float(new_target_weight)
            if reset_initial:
                goal.initial_weight = float(new_weight) if new_weight else goal.current_weight
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
        return redirect(url_for('main.profile'))

    # --- Calculate dynamic stats ---
    def calc_bmr(weight, height, gender, age=30):
        if not weight or not height or not gender:
            return None
        if gender == 'male':
            return 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == 'female':
            return 10 * weight + 6.25 * height - 5 * age - 161
        else:
            return 10 * weight + 6.25 * height - 5 * age

    bmr = None
    if goal.current_weight and user.height and user.gender:
        bmr = round(calc_bmr(goal.current_weight, user.height, user.gender))

    # BMR comparison: average BMR this week vs last week
    today = date.today()
    week_ago = today - timedelta(days=7)
    two_weeks_ago = today - timedelta(days=14)
    # Get daily metrics for last 14 days
    metrics = db.session.query(DailyMetrics).filter(
        DailyMetrics.user_id == user.id,
        DailyMetrics.date >= two_weeks_ago
    ).order_by(DailyMetrics.date.asc()).all()
    # Calculate BMR for each day if possible
    bmr_by_day = {}
    for m in metrics:
        if m.weight and user.height and user.gender:
            bmr_by_day[m.date] = calc_bmr(m.weight, user.height, user.gender)
    # Fill missing days with current profile BMR
    for i in range(14):
        d = two_weeks_ago + timedelta(days=i)
        if d not in bmr_by_day and bmr:
            bmr_by_day[d] = bmr
    # Average BMR for this week and last week
    this_week_bmrs = [bmr_by_day.get(two_weeks_ago + timedelta(days=i)) for i in range(7, 14)]
    last_week_bmrs = [bmr_by_day.get(two_weeks_ago + timedelta(days=i)) for i in range(0, 7)]
    this_week_bmrs = [v for v in this_week_bmrs if v]
    last_week_bmrs = [v for v in last_week_bmrs if v]
    bmr_change = ''
    if this_week_bmrs and last_week_bmrs:
        avg_this = sum(this_week_bmrs) / len(this_week_bmrs)
        avg_last = sum(last_week_bmrs) / len(last_week_bmrs)
        if avg_last != 0:
            percent = (avg_this - avg_last) / avg_last * 100
            color = 'green' if percent > 0 else 'red'
            sign = '+' if percent > 0 else ''
            bmr_change = f'<span class="text-{color}-600">{sign}{percent:.1f}% vs. last week</span>'

    # Net Daily Calories (today's intake - burn)
    calories_in = db.session.query(db.func.sum(CalorieEntry.calories)).filter_by(user_id=user.id, date=today).scalar() or 0
    calories_out = db.session.query(db.func.sum(CalorieBurn.calories_burned)).filter_by(user_id=user.id, date=today).scalar() or 0
    net_daily_calories = calories_in - calories_out
    # Net Daily Calories comparison: today vs yesterday
    yesterday = today - timedelta(days=1)
    yest_in = db.session.query(db.func.sum(CalorieEntry.calories)).filter_by(user_id=user.id, date=yesterday).scalar() or 0
    yest_out = db.session.query(db.func.sum(CalorieBurn.calories_burned)).filter_by(user_id=user.id, date=yesterday).scalar() or 0
    net_yesterday = yest_in - yest_out
    net_calories_change = ''
    if net_yesterday != 0:
        percent = (net_daily_calories - net_yesterday) / abs(net_yesterday) * 100
        color = 'green' if percent < 0 else 'red'  # less net calories is improvement
        sign = '+' if percent > 0 else ''
        net_calories_change = f'<span class="text-{color}-600">{sign}{percent:.1f}% vs. yesterday</span>'

    # Target Progress (using UserGoal)
    target_progress = None
    if goal.target_weight is not None and goal.initial_weight is not None and goal.target_weight != goal.initial_weight:
        target_progress = int(abs(goal.current_weight - goal.initial_weight) / abs(goal.target_weight - goal.initial_weight) * 100)
        target_progress = max(0, min(target_progress, 100))
    elif goal.target_weight == goal.initial_weight:
        target_progress = None
    return render_template('profile.html', title='Profile', current_user=user, bmr=bmr, bmr_change=bmr_change, net_daily_calories=net_daily_calories, net_calories_change=net_calories_change, target_progress=target_progress, initial_weight=goal.initial_weight, target_weight=goal.target_weight, current_weight=goal.current_weight)


@main.route('/complete-profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    user = User.query.get(session['user_id'])
    from .models import UserGoal
    goal = UserGoal.query.filter_by(user_id=user.id).first()
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
        # Ensure UserGoal is created with initial and current weight
        if not goal and weight:
            goal = UserGoal(user_id=user.id, initial_weight=float(weight), current_weight=float(weight))
            db.session.add(goal)
        try:
            db.session.commit()
            flash('Profile completed successfully!', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving profile: {str(e)}', 'error')
    return render_template('complete_profile.html', title='Complete Profile', current_user=user)

@main.route('/autocomplete')
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

    return jsonify(results[:10])  # Return only 10 results

