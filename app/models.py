from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy import Date
import sqlalchemy as sa
import sqlalchemy.orm as so
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import json
from sqlalchemy.ext.declarative import declarative_base


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    photo = db.Column(db.String(255), nullable=True)  # Store filename of profile photo
    gender = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    calorie_entries = db.relationship(
        'CalorieEntry', back_populates='user', cascade='all, delete-orphan')
    friendships_initiated = db.relationship(
        'Friendship', foreign_keys='Friendship.user_id', back_populates='user')
    friendships_received = db.relationship(
        'Friendship', foreign_keys='Friendship.friend_id', back_populates='friend')
    shared_calories_sent = db.relationship(
        'SharedCalories', foreign_keys='SharedCalories.sharer_id', back_populates='sharer')
    shared_calories_received = db.relationship(
        'SharedCalories', foreign_keys='SharedCalories.recipient_id', back_populates='recipient')
    daily_metrics = db.relationship(
        'DailyMetrics', back_populates='user', cascade='all, delete-orphan')
    calorie_burns = db.relationship(
        'CalorieBurn', back_populates='user', cascade='all, delete-orphan')
    verification_codes = db.relationship(
        'VerificationCode', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

class MealType(db.Model):
    __tablename__ = 'meal_types'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, nullable=False)
    display_name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    
    # Relationship
    calorie_entries: so.Mapped[List['CalorieEntry']] = so.relationship(
        back_populates='meal_type')

    def __repr__(self):
        return f'<MealType {self.display_name}>'

class CalorieEntry(db.Model):
    __tablename__ = 'calorie_entries'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    meal_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('meal_types.id'), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(Date, nullable=False)
    calories: so.Mapped[int] = so.mapped_column(nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    
    # Relationships
    user: so.Mapped['User'] = so.relationship(back_populates='calorie_entries')
    meal_type: so.Mapped['MealType'] = so.relationship(back_populates='calorie_entries')

    def __repr__(self):
        return f'<CalorieEntry {self.id} for user {self.user_id}>'

class Friendship(db.Model):
    __tablename__ = 'friendships'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    friend_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status: so.Mapped[str] = so.mapped_column(sa.String(20), default='pending', nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    
    # Relationships
    user: so.Mapped['User'] = so.relationship(foreign_keys=[user_id], back_populates='friendships_initiated')
    friend: so.Mapped['User'] = so.relationship(foreign_keys=[friend_id], back_populates='friendships_received')
    
    # Constraints
    __table_args__ = (
        sa.CheckConstraint('user_id != friend_id', name='check_user_not_friend'),
        sa.UniqueConstraint('user_id', 'friend_id', name='unique_friendship')
    )

    def __repr__(self):
        return f'<Friendship {self.user_id} -> {self.friend_id} ({self.status})>'

class SharedCalories(db.Model):
    __tablename__ = 'shared_calories'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sharer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    conditions: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False, default='{}')  # Store JSON as text
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    
    # Relationships
    sharer: so.Mapped['User'] = so.relationship(foreign_keys=[sharer_id], back_populates='shared_calories_sent')
    recipient: so.Mapped['User'] = so.relationship(foreign_keys=[recipient_id], back_populates='shared_calories_received')

    # Constraints to prevent sharing with self
    __table_args__ = (
        sa.CheckConstraint('sharer_id != recipient_id', name='check_not_share_with_self'),
    )

    def __repr__(self):
        return f'<SharedCalories {self.sharer_id} -> {self.recipient_id}>'

# New models based on 1.md
class DailyMetrics(db.Model):
    __tablename__ = 'daily_metrics'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(Date, nullable=False)
    weight: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    sleep_hours: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    mood: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    
    # Relationship
    user: so.Mapped['User'] = so.relationship(back_populates='daily_metrics')
    
    # Unique constraint for one entry per user per day
    __table_args__ = (
        sa.UniqueConstraint('user_id', 'date', name='unique_user_date_metrics'),
    )
    
    def __repr__(self):
        return f'<DailyMetrics for user {self.user_id} on {self.date}>'

class ExerciseType(db.Model):
    __tablename__ = 'exercise_types'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, nullable=False)
    display_name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    
    # Relationship
    calorie_burns: so.Mapped[List['CalorieBurn']] = so.relationship(
        back_populates='exercise_type')

    def __repr__(self):
        return f'<ExerciseType {self.display_name}>'

class CalorieBurn(db.Model):
    __tablename__ = 'calorie_burns'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(Date, nullable=False)
    exercise_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('exercise_types.id'), nullable=False)
    duration: so.Mapped[int] = so.mapped_column(nullable=False)  # in minutes
    calories_burned: so.Mapped[Optional[int]] = so.mapped_column(nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    
    # Relationships
    user: so.Mapped['User'] = so.relationship(back_populates='calorie_burns')
    exercise_type: so.Mapped['ExerciseType'] = so.relationship(back_populates='calorie_burns')
    
    def __repr__(self):
        return f'<CalorieBurn {self.exercise_type.display_name} for user {self.user_id} on {self.date}>'

class VerificationCode(db.Model):
    __tablename__ = 'verification_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=30), nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationship
    user = db.relationship('User', back_populates='verification_codes')
    
    def __repr__(self):
        return f'<VerificationCode for user {self.user_id}>'
    
    def is_valid(self):
        return not self.is_used and datetime.utcnow() < self.expires_at

# Create indexes (SQLAlchemy 2.0 style)
sa.Index('idx_entries_user_date', CalorieEntry.user_id, CalorieEntry.date)
sa.Index('idx_shared_conditions', SharedCalories.recipient_id, SharedCalories.created_at)
sa.Index('idx_friendships_status', Friendship.user_id, Friendship.status)
sa.Index('idx_daily_metrics_user_date', DailyMetrics.user_id, DailyMetrics.date)
sa.Index('idx_calorie_burns_user_date', CalorieBurn.user_id, CalorieBurn.date)
sa.Index('idx_verification_codes', VerificationCode.user_id, VerificationCode.code)

   