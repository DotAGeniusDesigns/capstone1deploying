from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError

mbti_choices = [
    ('', 'Select MBTI Type'),
    ('INTJ', 'INTJ'), ('INTP', 'INTP'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
    ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
    ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
    ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP')
]

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    mbti = SelectField('MBTI Type', choices=mbti_choices, validators=[Optional()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mbti = SelectField('MBTI Type', choices=mbti_choices, validators=[Optional()])
    submit = SubmitField('Update Account')
