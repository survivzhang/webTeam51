from . import app, db
from flask import render_template, request, url_for, redirect, flash, session, jsonify
import sqlalchemy as sa
from .models import User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegistrationForm
from .auth import login_required, valid_login, valid_register, valid_regist
import traceback
import os
import sqlite3

# Home/Auth routes
@app.route('/')
@app.route('/index')
def index():
    login_form = LoginForm()
    register_form = RegistrationForm()
    return render_template('index.html', title='Login', login_form=login_form, register_form=register_form)


@app.route('/login', methods=['POST'])
def login():
    # Try to get data from JSON or form data
    data = request.get_json(silent=True)  # Use silent=True to avoid exceptions
    if not data:
        data = request.form  # If JSON parsing fails, try to get from form data

    # Get email and password from the form (form uses "email" instead of "identifier")
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    # Check if email is username or email
    if '@' in email:
        user = User.query.filter_by(email=email).first()
    else:
        user = User.query.filter_by(username=email).first()

    # Verify if user exists and password is correct
    if user and check_password_hash(user.password_hash, password):
        # Login success, record user ID in session
        session['user_id'] = user.id
        # Redirect to sharing interface
        return redirect(url_for('sharing'))
    else:
        flash('Invalid email/username or password', 'error')
        return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    login_form = LoginForm()
    register_form = RegistrationForm()
    
    # Debug: Print database file path
    from webTeam51.config import Config
    db_path = Config.SQLALCHEMY_DATABASE_URI
    print(f"Database path: {db_path}")
    db_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.db')
    print(f"Database file exists: {os.path.exists(db_file_path)}")
    
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        
        try:
            # Check if username and email already exist
            if not valid_regist(username, email):
                flash('Username or email already exists', 'error')
                return redirect(url_for('index'))
            
            try:
                # Create new user
                new_user = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password),
                    created_at=datetime.utcnow()
                )
                
                # Debug print
                print(f"Creating user: {username}, email: {email}")
                
                # Add to session
                db.session.add(new_user)
                
                # Explicitly flush to check for errors before commit
                db.session.flush()
                
                # Commit changes
                db.session.commit()
                
                # Verify user in database
                saved_user = db.session.execute(
                    sa.select(User).where(User.username == username)
                ).scalar_one_or_none()
                
                if saved_user:
                    print(f"User created and verified, ID: {saved_user.id}")
                else:
                    print("Error: User not found in database after commit!")
                    # Try direct SQL as fallback
                    try:
                        direct_insert_user(username, email, password)
                    except Exception as sql_error:
                        print(f"Direct SQL insertion also failed: {str(sql_error)}")
                
                flash('Registration successful! You can now log in', 'success')
                return redirect(url_for('index'))
            
            except Exception as orm_error:
                db.session.rollback()
                print(f"ORM error: {str(orm_error)}")
                
                # Try direct SQL insertion as fallback
                try:
                    direct_insert_user(username, email, password)
                    flash('Registration successful! You can now log in', 'success')
                    return redirect(url_for('index'))
                except Exception as sql_error:
                    print(f"Direct SQL insertion also failed: {str(sql_error)}")
                    raise orm_error  # Rethrow original error
        
        except Exception as e:
            db.session.rollback()
            error_details = traceback.format_exc()
            print(f"Registration error: {str(e)}\n{error_details}")
            flash(f'Error during registration process: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    # If form validation fails, show errors
    for field, errors in register_form.errors.items():
        for error in errors:
            flash(f"{error}", 'error')
    
    return render_template('index.html', title='Login', login_form=login_form, register_form=register_form)


def direct_insert_user(username, email, password):
    """Insert user directly using SQL (if SQLAlchemy ORM fails)"""
    hashed_password = generate_password_hash(password)
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.db'))
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, hashed_password, now)
        )
        conn.commit()
        inserted_id = cursor.lastrowid
        print(f"User directly inserted, ID: {inserted_id}")
        return inserted_id
    finally:
        conn.close()


@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('index'))
