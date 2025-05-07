from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User
import sqlalchemy as sa
from . import db

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    # Removing validation to simplify debugging
    # def validate_email(self, email):
    #     """Validate email exists in the database"""
    #     user = db.session.execute(
    #         sa.select(User).where(User.username == email.data)
    #     ).scalar_one_or_none()
    #     
    #     if not user:
    #         raise ValidationError('Email address not registered')

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=2, max=30, message="Username must be between 2 and 30 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=6, message="Password must be at least 6 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    verification_code = StringField('Verification Code', validators=[
        DataRequired(message="Verification code is required"),
        Length(min=6, max=6, message="Verification code must be 6 characters")
    ])
    submit = SubmitField('Register')
    
    # Removing validation to simplify debugging
    # def validate_email(self, email):
    #     """Validate email is not already registered"""
    #     user = db.session.execute(
    #         sa.select(User).where(User.username == email.data)
    #     ).scalar_one_or_none()
    #     
    #     if user:
    #         raise ValidationError('Email address already registered')