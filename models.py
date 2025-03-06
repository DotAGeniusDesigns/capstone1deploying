from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mbti = db.Column(db.String(4))
    chinese_zodiac = db.Column(db.String(20))
    last_fortune = db.Column(db.Text)
    last_fortune_date = db.Column(db.Date)
    role = db.Column(db.String(20), default='user')

class DailyFortune(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zodiac_sign = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    fortune = db.Column(db.Text, nullable=False)

class MBTITrait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(4), unique=True, nullable=False)
    strengths = db.Column(db.Text, nullable=False)
    weaknesses = db.Column(db.Text, nullable=False)

class ChineseZodiac(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sign = db.Column(db.String(20), unique=True, nullable=False)
    yearly_fortune_2024 = db.Column(db.Text, nullable=False)
