from typing import Optional, List
from datetime import datetime, date
from sqlalchemy import Date
import sqlalchemy as sa
import sqlalchemy.orm as so
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import json
from sqlalchemy.ext.declarative import declarative_base


class User(db.Model):
    __tablename__ = 'users'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(80), unique=True, nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    
    # Relationships
    calorie_entries: so.Mapped[List['CalorieEntry']] = so.relationship(
        back_populates='user', cascade='all, delete-orphan')
    friendships_initiated: so.Mapped[List['Friendship']] = so.relationship(
        foreign_keys='Friendship.user_id', back_populates='user')
    friendships_received: so.Mapped[List['Friendship']] = so.relationship(
        foreign_keys='Friendship.friend_id', back_populates='friend')
    shared_calories_sent: so.Mapped[List['SharedCalories']] = so.relationship(
        foreign_keys='SharedCalories.sharer_id', back_populates='sharer')
    shared_calories_received: so.Mapped[List['SharedCalories']] = so.relationship(
        foreign_keys='SharedCalories.recipient_id', back_populates='recipient')

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
    date: so.Mapped[date] = so.mapped_column(Date, nullable=False)
    calories: so.Mapped[int] = so.mapped_column(nullable=False)
    food_detail: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    photo_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
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

# Create indexes (SQLAlchemy 2.0 style)
sa.Index('idx_entries_user_date', CalorieEntry.user_id, CalorieEntry.date)
sa.Index('idx_shared_conditions', SharedCalories.recipient_id, SharedCalories.created_at)
sa.Index('idx_friendships_status', Friendship.user_id, Friendship.status)

   