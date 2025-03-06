from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db, User, DailyFortune, MBTITrait, ChineseZodiac
from forms import LoginForm, RegistrationForm, EditAccountForm
from datetime import datetime, timezone
from openai import OpenAI
from dotenv import load_dotenv
from functools import wraps
import requests
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Ensure proper context is pushed
with app.app_context():
    db.create_all()

# Admin role required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in and is an admin
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('daily_fortune'))
        
        return f(*args, **kwargs)
    return decorated_function

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to daily_fortune
    if 'user_id' in session:
        return redirect(url_for('daily_fortune'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            # Set admin status in session
            session['is_admin'] = (user.role == 'admin')
            flash('Login successful!', 'success')
            return redirect(url_for('daily_fortune'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to daily_fortune
    if 'user_id' in session:
        return redirect(url_for('daily_fortune'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(name=form.name.data, birthday=form.birthday.data, username=form.username.data,
                        email=form.email.data, password=hashed_password, mbti=form.mbti.data)
        new_user.chinese_zodiac = get_chinese_zodiac(new_user.birthday.year)
        # First user is admin, others are normal users
        if User.query.count() == 0:
            new_user.role = 'admin'
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    user = User.query.get(session['user_id'])
    form = EditAccountForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.birthday = form.birthday.data
        user.username = form.username.data
        user.email = form.email.data
        user.mbti = form.mbti.data
        user.chinese_zodiac = get_chinese_zodiac(user.birthday.year)

        db.session.commit()
        flash('Your account has been updated successfully!', 'success')
        return redirect(url_for('daily_fortune'))

    return render_template('edit_account.html', form=form)

def get_zodiac_sign(day, month):
    """
    Get the zodiac sign based on birth day and month
    
    Args:
        day (int): Day of birth
        month (int): Month of birth
        
    Returns:
        str: The zodiac sign
    """
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "scorpio"
    else:
        return "sagittarius"

def get_chinese_zodiac(year):
    """
    Get the Chinese zodiac sign based on birth year
    
    Args:
        year (int): Year of birth
        
    Returns:
        str: The Chinese zodiac sign
    """
    zodiacs = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Sheep", "Monkey", "Rooster", "Dog", "Pig"]
    return zodiacs[(year - 4) % 12]

def generate_unique_fortune(astrological_fortune, mbti_strengths, mbti_weaknesses, chinese_zodiac_fortune):
    """
    Generate a unique fortune using AI based on various attributes
    
    Args:
        astrological_fortune (str): Daily astrological fortune
        mbti_strengths (str): MBTI personality strengths
        mbti_weaknesses (str): MBTI personality weaknesses
        chinese_zodiac_fortune (str): Chinese zodiac fortune
        
    Returns:
        str: Generated unique fortune
    """
    prompt = f""" 
    Astrological Fortune: {astrological_fortune}
    MBTI Strengths: {mbti_strengths}
    MBTI Weaknesses: {mbti_weaknesses}
    Chinese Zodiac Fortune: {chinese_zodiac_fortune}

    Generate a unique daily fortune for user, using mainly the daily astrological fortune, but incorporate some of the other factors, and keep it under 70 words.
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that generates unique daily fortunes for users."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content.strip()

@app.route('/daily_fortune')
@login_required
def daily_fortune():
    user = User.query.get(session['user_id'])
    today = datetime.now(timezone.utc).date()
    birthday = user.birthday
    zodiac_sign = get_zodiac_sign(birthday.day, birthday.month)

    # Check if the fortune has already been generated today
    if user.last_fortune and user.last_fortune_date == today:
        fortune = user.last_fortune
        chinese_zodiac_fortune_record = ChineseZodiac.query.filter_by(sign=user.chinese_zodiac).first()
        chinese_zodiac_fortune = chinese_zodiac_fortune_record.yearly_fortune_2024 if chinese_zodiac_fortune_record else 'No fortune available.'
    else:
        fortune_record = DailyFortune.query.filter_by(zodiac_sign=zodiac_sign, date=today).first()
        if fortune_record:
            astrological_fortune = fortune_record.fortune
        else:
            astrological_fortune = 'Unable to fetch your fortune. Please try again later.'

        chinese_zodiac_fortune_record = ChineseZodiac.query.filter_by(sign=user.chinese_zodiac).first()
        chinese_zodiac_fortune = chinese_zodiac_fortune_record.yearly_fortune_2024 if chinese_zodiac_fortune_record else 'No fortune available.'

        mbti_trait_record = MBTITrait.query.filter_by(type=user.mbti).first()
        mbti_strengths = mbti_trait_record.strengths if mbti_trait_record else 'No strengths available.'
        mbti_weaknesses = mbti_trait_record.weaknesses if mbti_trait_record else 'No weaknesses available.'

        fortune = generate_unique_fortune(astrological_fortune, mbti_strengths, mbti_weaknesses, chinese_zodiac_fortune)
        
        # Store the generated fortune and the date
        user.last_fortune = fortune
        user.last_fortune_date = today
        db.session.commit()
        flash('Your daily fortune has been generated!', 'info')

    current_date_str = datetime.now().strftime('%B %d, %Y')
    return render_template('fortune.html', user=user, zodiac_sign=zodiac_sign, current_date=current_date_str, fortune=fortune, chinese_zodiac_fortune=chinese_zodiac_fortune)


@app.route('/generate_fortunes', methods=['GET', 'POST'])
@admin_required
def generate_fortunes():
    if request.method == 'POST':
        zodiac_signs = ["capricorn", "aquarius", "pisces", "aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius"]
        url = "https://horoscope-astrology.p.rapidapi.com/horoscope?day=today&sunsign={}"
        headers = {
            'x-rapidapi-host': "horoscope-astrology.p.rapidapi.com",
            'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
        }

        for sign in zodiac_signs:
            response = requests.get(url.format(sign), headers=headers)
            if response.status_code == 200:
                data = response.json()
                fortune = data.get('horoscope', 'No fortune available today.')
                new_fortune = DailyFortune(zodiac_sign=sign, fortune=fortune)
                db.session.add(new_fortune)
        
        db.session.commit()
        flash('Daily fortunes have been generated successfully!', 'success')
        return redirect(url_for('generate_fortunes'))
    
    return render_template('generate_fortunes.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
