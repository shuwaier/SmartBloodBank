import re 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from SmartBloodBank.models import User, Campaign, Hospital
from SmartBloodBank import db 
from SmartBloodBank.models import City
from flask_wtf.file import FileField, FileAllowed










class DonorRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])

    city = SelectField('City', validators=[DataRequired()], choices=[('riyadh', 'Riyadh Province -  الرياض'), ('jeddah', 'Jeddah Province -  جدة'),
     ('medinah', 'Medinah Province -  المدينة'), ('makkah', 'Makkah Province - مكة'), ('qassim', 'Qassim Province - القصيم'),
      ('easter', 'Easter Province - المنطقه الشرقيه'), ('asir', 'Asir Province -  عسير'), ('tabuk', 'Tabuk Province -  تبوك'),
       ('hail', 'Hail Province -  حايل'), ('northern', 'Norther Borders -  منطقة الحدود الشماليه'), ('jizan', 'Jizan Province -  جيزان'),
        ('tabuk', 'Tabuk Province -  تبوك'), ('bahah', 'Bahah Province -  الباحة'), ('najran', 'Najran Province -  نجران')])

    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    confirm_password = PasswordField('Confirm Password' , validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired()])
    blood_type = SelectField('Blood Typejhgjg', choices=[('o-', 'O-'), ('o+', 'O+'), ('a-', 'A-'), ('a+', 'A+'), ('b-', 'B-'), ('b+', 'B+'), ('ab-', 'AB-'), ('ab+', 'AB+')])
    first_name = StringField('First Name')
    last_name  = StringField('Last Name')

    submit = SubmitField('Sign Up')


        

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Thats email is taken. please choose another one.!')






class LeaderRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    
    city = SelectField('City', validators=[DataRequired()], choices=[('riyadh', 'Riyadh Province -  الرياض'), ('jeddah', 'Jeddah Province -  جدة'),
     ('medinah', 'Medinah Province -  المدينة'), ('makkah', 'Makkah Province - مكة'), ('qassim', 'Qassim Province - القصيم'),
      ('easter', 'Easter Province - المنطقه الشرقيه'), ('asir', 'Asir Province -  عسير'), ('tabuk', 'Tabuk Province -  تبوك'),
       ('hail', 'Hail Province -  حايل'), ('northern', 'Norther Borders -  منطقة الحدود الشماليه'), ('jizan', 'Jizan Province -  جيزان'),
        ('tabuk', 'Tabuk Province -  تبوك'), ('bahah', 'Bahah Province -  الباحة'), ('najran', 'Najran Province -  نجران')])

    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    confirm_password = PasswordField('Confirm Password' , validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])
    first_name = StringField('First Name',)
    last_name  = StringField('Last Name')

    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Thats username is taken. please choose another one.!')
        
        

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Thats email is taken. please choose another one.!')


class LoginForm(FlaskForm):
    email = StringField('Email' , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    submit = SubmitField('Login')

    

    


class UpdateAccountForm(FlaskForm):
    phone = StringField('Phone', validators=[Length(min=10, max=10)])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')

    city = SelectField('City', choices=[('riyadh', 'Riyadh Province -  الرياض'), ('jeddah', 'Jeddah Province -  جدة'),
     ('medinah', 'Medinah Province -  المدينة'), ('makkah', 'Makkah Province - مكة'), ('qassim', 'Qassim Province - القصيم'),
      ('easter', 'Easter Province - المنطقه الشرقيه'), ('asir', 'Asir Province -  عسير'), ('tabuk', 'Tabuk Province -  تبوك'),
       ('hail', 'Hail Province -  حايل'), ('northern', 'Norther Borders -  منطقة الحدود الشماليه'), ('jizan', 'Jizan Province -  جيزان'),
        ('tabuk', 'Tabuk Province -  تبوك'), ('bahah', 'Bahah Province -  الباحة'), ('najran', 'Najran Province -  نجران')])

    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])


    submit = SubmitField('Update')




class InviteForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Invite Friend')
    


class ConfirmDonation(FlaskForm):
    email = StringField('Donor Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Confirm Donation')

    def check_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            pass
        else:
            raise ValidationError('This donor does not exist or the email is wrong')


class RequestBloodForm(FlaskForm):
    city = SelectField('City', choices=[('riyadh', 'Riyadh Province -  الرياض'), ('jeddah', 'Jeddah Province -  جدة'),
     ('medinah', 'Medinah Province -  المدينة'), ('makkah', 'Makkah Province - مكة'), ('qassim', 'Qassim Province - القصيم'),
      ('easter', 'Easter Province - المنطقه الشرقيه'), ('asir', 'Asir Province -  عسير'), ('tabuk', 'Tabuk Province -  تبوك'),
       ('hail', 'Hail Province -  حايل'), ('northern', 'Norther Borders -  منطقة الحدود الشماليه'), ('jizan', 'Jizan Province -  جيزان'),
        ('tabuk', 'Tabuk Province -  تبوك'), ('bahah', 'Bahah Province -  الباحة'), ('najran', 'Najran Province -  نجران')])

    blood_type = SelectField('Blood Type', choices=[('o-', 'O-'), ('o+', 'O+'), ('a-', 'A-'), ('a+', 'A+'), ('b-', 'B-'), ('b+', 'B+'), ('ab-', 'AB-'), ('ab+', 'AB+')])
    comment = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Request')
