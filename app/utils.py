import random
import string
from flask_mail import Message
from app import mail
from flask import render_template
import logging
import traceback

def generate_verification_code(length=6):
    """Generate a random verification code of specified length."""
    characters = string.digits
    return ''.join(random.choice(characters) for i in range(length))

def send_verification_email(user, verification_code):
    """Send verification email to user with the provided code."""
    try:
        msg = Message(
            subject="Welcome to CalTrack - Email Verification",
            recipients=[user.email],
            sender=("CalTrack", "caltrack1@outlook.com")
        )
        
        # Use simple text content as fallback
        msg.body = f"""
Hello {user.username},

Welcome to CalTrack! We're excited to have you join our community of health enthusiasts.

To complete your registration, please use this verification code: {verification_code}

This code will expire in 30 minutes.

Best regards,
The CalTrack Team
"""
        
        # Add HTML content
        try:
            msg.html = render_template(
                'emails/verification.html',
                username=user.username,
                code=verification_code
            )
        except Exception as html_error:
            print(f"Error rendering HTML template: {str(html_error)}")
            # Continue with plain text only
        
        # Print debug information
        print(f"Sending email to: {user.email}")
        print(f"Using SMTP settings: Server={mail.app.config.get('MAIL_SERVER')}, Port={mail.app.config.get('MAIL_PORT')}")
        print(f"TLS={mail.app.config.get('MAIL_USE_TLS')}, SSL={mail.app.config.get('MAIL_USE_SSL')}")
        
        # For development, also log the verification code
        print(f"======= VERIFICATION CODE =======")
        print(f"TO: {user.email}")
        print(f"CODE: {verification_code}")
        print(f"=================================")
        
        # Actually send the email
        mail.send(msg)
        print(f"Email sent successfully to {user.email}")
        return True
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error sending email: {str(e)}\n{error_details}")
        return False 