from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import db


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    sign_in = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_check = PasswordField('Reenter Password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

    def validate_email(self, email):  # custom validator auto-applied to email
        user_from_db = db.users.find_one({"email": email.data})
        if user_from_db is not None:
            raise ValidationError('This email address is already in use.')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')


class SetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_check = PasswordField('Reenter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
