from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name ')
    username = StringField('Username ', [validators.DataRequired()])
    email = StringField('Email ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password ', [validators.DataRequired(),validators.Length(min=6), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password ', [validators.DataRequired()])
    country = StringField('Country ', [validators.DataRequired()])
    city = StringField('City ', [validators.DataRequired()])
    contact = StringField('Contact ', [validators.DataRequired()])
    address = StringField('Address ', [validators.DataRequired()])
    zipcode = StringField('Zip code ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


class LoginForm(FlaskForm):
    email = StringField('Email ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password ', [validators.DataRequired()])



class ChangePasswordForm(FlaskForm):
    email = StringField('Email ', [validators.Email(), validators.DataRequired()])

class CustomerUpdateForm(FlaskForm):
    name = StringField('Name ')
    username = StringField('Username ', [validators.DataRequired()])
    email = StringField('Email  ', [validators.Email(), validators.DataRequired()])
    country = StringField('Country ', [validators.DataRequired()])
    city = StringField('City ', [validators.DataRequired()])
    contact = StringField('Contact ', [validators.DataRequired()])
    address = StringField('Address ', [validators.DataRequired()])
    zipcode = StringField('Zip code ', [validators.DataRequired()])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")
