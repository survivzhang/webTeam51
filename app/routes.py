from flask import render_template, request, url_for, redirect, flash, session, jsonify, current_app
import sqlalchemy as sa
from .models import User, VerificationCode
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegistrationForm
from .auth import login_required, valid_login, valid_register, valid_regist
from .utils import generate_verification_code, send_verification_email
from .blueprints import main
from . import db
import traceback
import os
import sqlite3
from werkzeug.utils import secure_filename
import uuid

# Allowed file extensions for profile photos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home/Auth routes
@main.route('/')
@main.route('/index')
def index():
    login_form = LoginForm()
    register_form = RegistrationForm()
    return render_template('index.html', title='Login', login_form=login_form, register_form=register_form)


@main.route('/login', methods=['POST'])
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
        return redirect(url_for('main.home'))
    else:
        flash('Invalid email/username or password', 'error')
        return redirect(url_for('main.index'))


@main.route('/register', methods=['POST'])
def register():
    login_form = LoginForm()
    register_form = RegistrationForm()
    
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        verification_code = register_form.verification_code.data
        
        # 在测试环境中，如果使用了固定验证码123456，直接通过验证
        is_test_mode = current_app.config.get('TESTING', False)
        if is_test_mode and verification_code == "123456":
            print("TEST MODE: Bypassing verification code check")
            # 创建新用户
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                created_at=datetime.utcnow(),
                is_verified=True
            )
            db.session.add(new_user)
            db.session.commit()
            
            # 登录用户
            session['user_id'] = new_user.id
            flash('Registration successful! Please complete your profile.', 'success')
            return redirect(url_for('main.complete_profile'))
        
        # 正常验证流程
        # Verify that we have a verification code in session
        if 'verification_code' not in session or session.get('verification_code') != verification_code:
            flash('Invalid verification code', 'error')
            return redirect(url_for('main.index'))
        
        # Verify that the code hasn't expired (30 minutes)
        if 'code_created_at' in session:
            code_time = datetime.fromisoformat(session['code_created_at'])
            if (datetime.utcnow() - code_time).total_seconds() > 1800:  # 30 minutes
                flash('Verification code has expired. Please request a new one', 'error')
                return redirect(url_for('main.index'))
        
        try:
            # Get the temporary user ID from session
            temp_user_id = session.get('temp_user_id')
            
            if not temp_user_id:
                flash('No verification code has been requested. Please request a code first.', 'error')
                return redirect(url_for('main.index'))
            
            # Find the temporary user
            temp_user = User.query.get(temp_user_id)
            
            if not temp_user:
                flash('Registration session expired. Please start again.', 'error')
                return redirect(url_for('main.index'))
            
            try:
                # Find the verification code record
                verification_record = VerificationCode.query.filter_by(
                    user_id=temp_user_id,
                    code=verification_code,
                    is_used=False
                ).first()
                
                if not verification_record:
                    flash('Invalid verification code. Please try again.', 'error')
                    return redirect(url_for('main.index'))
                
                # Update the temporary user to be a permanent user
                temp_user.password_hash = generate_password_hash(password)
                temp_user.is_verified = True
                
                # Mark the verification code as used
                verification_record.is_used = True
                
                # Commit the changes
                db.session.commit()
                
                print(f"User verified, ID: {temp_user.id}")
                print(f"Verification code {verification_code} marked as used")
                
                # Clear verification data from session
                session.pop('temp_username', None)
                session.pop('temp_email', None)
                session.pop('verification_code', None)
                session.pop('code_created_at', None)
                session.pop('temp_user_id', None)
                
                # Log in the user and redirect to complete-profile
                session['user_id'] = temp_user.id
                flash('Registration successful! Please complete your profile.', 'success')
                return redirect(url_for('main.complete_profile'))
                
            except Exception as orm_error:
                db.session.rollback()
                print(f"ORM error: {str(orm_error)}")
                flash(f'Error during registration: {str(orm_error)}', 'error')
                return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            error_details = traceback.format_exc()
            print(f"Registration error: {str(e)}\n{error_details}")
            flash(f'Error during registration process: {str(e)}', 'error')
            return redirect(url_for('main.index'))
    
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


@main.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('main.index'))


@main.route('/profile/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    if 'photo' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('main.profile'))
    
    file = request.files['photo']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('main.profile'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Allowed types: PNG, JPG, JPEG, GIF', 'error')
        return redirect(url_for('main.profile'))
    
    try:
        # Create profile_photos directory if it doesn't exist
        upload_folder = os.path.join(current_app.static_folder, 'profile_photos')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Save the file
        file.save(file_path)
        
        # Update user's photo in database
        user = User.query.get(session['user_id'])
        if user.photo:  # Delete old photo if exists
            old_photo_path = os.path.join(upload_folder, user.photo)
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)
        
        user.photo = unique_filename
        db.session.commit()
        
        flash('Profile photo updated successfully', 'success')
    except Exception as e:
        flash(f'Error uploading photo: {str(e)}', 'error')
        print(f"Error in upload_photo: {str(e)}")
        print(traceback.format_exc())
    
    return redirect(url_for('main.profile'))

@main.route('/send-verification', methods=['POST'])
def send_verification():
    """Send verification code to email during registration process"""
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        
        # Validate input
        if not email or not username:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Email and username are required'}), 400
            flash('Email and username are required', 'error')
            return redirect(url_for('main.index'))
        
        # Check if email or username already exists
        if not valid_regist(username, email):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Username or email already exists'}), 400
            flash('Username or email already exists', 'error')
            return redirect(url_for('main.index'))
        
        # Store temporary user info in session
        session['temp_username'] = username
        session['temp_email'] = email
        
        # Generate verification code
        verification_code = generate_verification_code()
        session['verification_code'] = verification_code
        session['code_created_at'] = datetime.utcnow().isoformat()
        
        # Create a mock user for the email template
        mock_user = type('obj', (object,), {
            'email': email,
            'username': username
        })
        
        try:
            # Create temporary user record to associate with verification code
            temp_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash('temporary'),  # Temporary placeholder
                created_at=datetime.utcnow(),
                is_verified=False
            )
            db.session.add(temp_user)
            db.session.flush()  # Get ID without committing
            
            # Create verification code record in database
            verification_record = VerificationCode(
                user_id=temp_user.id,
                code=verification_code,
                created_at=datetime.fromisoformat(session['code_created_at']),
                expires_at=datetime.fromisoformat(session['code_created_at']) + timedelta(minutes=30),
                is_used=False  # Mark as unused initially
            )
            db.session.add(verification_record)
            db.session.commit()
            print(f"Verification code {verification_code} saved to database for temp user {temp_user.id}")
            print(f"Session verification_code: {session.get('verification_code')}")
            
            # Store temp user ID in session
            session['temp_user_id'] = temp_user.id
            
            # 在测试环境中，可以跳过实际发送邮件
            if current_app.config.get('TESTING', False):
                print(f"TESTING MODE: Skipping email send. Verification code: {verification_code}")
                success = True
                # 在测试环境中，将验证码显示在页面上，方便测试捕获
                flash(f"TESTING MODE: Skipping email send. Verification code: {verification_code}", "info")
            else:
                # Send verification email
                success = send_verification_email(mock_user, verification_code)
                
            if success:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    # 在测试环境中，通过AJAX响应返回验证码
                    if current_app.config.get('TESTING', False):
                        return jsonify({
                            'message': 'Verification code has been sent to your email',
                            'testing_code': verification_code
                        }), 200
                    else:
                        return jsonify({'message': 'Verification code has been sent to your email'}), 200
                flash('Verification code has been sent to your email', 'success')
            else:
                db.session.rollback()  # Roll back if email fails
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': 'Error sending verification email. Please try again.'}), 500
                flash('Error sending verification email. Please try again.', 'error')
        except Exception as e:
            db.session.rollback()
            print(f"Error sending email or creating verification record: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Error sending verification email. Please try again.'}), 500
            flash('Error sending verification email. Please try again.', 'error')
        
        return redirect(url_for('main.index'))
    


