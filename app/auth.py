from functools import wraps
from flask import session, redirect, url_for, flash, request, g
from sqlalchemy import and_, or_
from .models import User
from . import db
import sqlalchemy as sa
from werkzeug.security import check_password_hash

def login_required(f):
    """
    Decorator to ensure a user is logged in before accessing a route.
    If not logged in, redirects to the login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def valid_login(username, password):
    """Validate login information"""
    user = db.session.execute(
        sa.select(User).where(User.username == username)
    ).scalar_one_or_none()
    
    if user and check_password_hash(user.password_hash, password):
        return True, user
    return False, None

def valid_register(username):
    """Verify if username (email) is already registered"""
    user = db.session.execute(
        sa.select(User).where(User.username == username)
    ).scalar_one_or_none()
    
    if user:
        return False  # Already exists, registration not allowed
    return True  # Doesn't exist, registration allowed

# Registration verification (username and email validation)
def valid_regist(username, email):
    """Verify if both username and email are already registered by verified users"""
    user = db.session.execute(
        sa.select(User).where(
            and_(
                or_(User.username == username, User.email == email),
                User.is_verified == True  # Only check verified users
            )
        )
    ).scalar_one_or_none()
    
    if user:
        return False  # Already exists, registration not allowed
    return True  # Doesn't exist, registration allowed