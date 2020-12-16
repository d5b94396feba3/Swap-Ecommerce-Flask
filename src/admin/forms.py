from wtforms import Form, BooleanField, StringField, PasswordField, validators,ValidationError
from .models import User
from flask_wtf import FlaskForm

class RegistrationForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    access = StringField('Accessibility', [validators.Length(min=4, max=10)])
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")
