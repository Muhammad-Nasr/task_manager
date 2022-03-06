from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, SubmitField,EmailField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Email, EqualTo, Length, ValidationError
from wtforms.validators import DataRequired
from flask_login import current_user
from main.dbmodel import User




class RegisterForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(), Length(max=20, min=2)])
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6)])
    repeat_password = PasswordField(label='Repeate Password', validators=[DataRequired(), EqualTo(fieldname='password')])
    submit = SubmitField(label='Submit')


    def validate_username(self, username):
        attempted_user = User.query.filter_by(user_name=username.data).first()
        if attempted_user:
            raise ValidationError(message='Sorry, the username is already exist')

    def validate_email(self, email):
        attempted_user = User.query.filter_by(email=email.data).first()
        if attempted_user:
            raise ValidationError(message='The Email is already, exist, try log in')




class LoginForm(FlaskForm):
    email = StringField(label='Email')
    password= PasswordField(label='Password')
    submit = SubmitField(label='Log In')






class EditAccountForm(FlaskForm):

    username = StringField(label='User Name', validators=[Length(max=20, min=2)])
    email = EmailField(label='Email', validators=[ Email()])
    photo = FileField(label="Upload_Photo", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Edit')

    def validate_username(self, username):
        if username.data != current_user.user_name:
            attempted_user = User.query.filter_by(user_name=username.data).first()
            if attempted_user:
                raise ValidationError(message='Sorry, the username is already exist')

    def validate_email(self, email):
        if email.data != current_user.email:
            attempted_user = User.query.filter_by(email=email.data).first()
            if attempted_user:
                raise ValidationError(message='The Email is already, exist, try log in')



# create reset password form
class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6)])
    repeat_password = PasswordField(label='Repeate Password',
                                    validators=[DataRequired(), EqualTo(fieldname='password')])
    submit = SubmitField(label='Reset Password')


class EmailResetForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Send Email')

    def validate_email(self, email):
        attempted_user = User.query.filter_by(email=email.data).first()
        if not attempted_user:
            raise ValidationError(message='The Email is not exist, you should register first')



