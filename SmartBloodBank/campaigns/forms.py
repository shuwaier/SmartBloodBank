import re 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from SmartBloodBank.models import User, Campaign, Hospital
from SmartBloodBank import db 
from SmartBloodBank.models import City
from flask_wtf.file import FileField, FileAllowed






class CampaignForm(FlaskForm):
    name = StringField('Capmaign Name', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email' , validators=[DataRequired(), Email()])
    lat = StringField('lat', validators=[DataRequired()])
    lng = StringField('lng', validators=[DataRequired()])
    needed_blood =SelectField('Blood Type / Priority', choices=[('o-', 'O-'), ('o+', 'O+'), ('a-', 'A-'), ('a+', 'A+'),
                                             ('b-', 'B-'), ('b+', 'B+'), ('ab-', 'AB-'), ('ab+', 'AB+')])

    city = SelectField('City', choices=[('riyadh', 'Riyadh Province -  الرياض'), ('jeddah', 'Jeddah Province -  جدة'),
     ('medinah', 'Medinah Province -  المدينة'), ('makkah', 'Makkah Province - مكة'), ('qassim', 'Qassim Province - القصيم'),
      ('easter', 'Easter Province - المنطقه الشرقيه'), ('asir', 'Asir Province -  عسير'), ('tabuk', 'Tabuk Province -  تبوك'),
       ('hail', 'Hail Province -  حايل'), ('northern', 'Norther Borders -  منطقة الحدود الشماليه'), ('jizan', 'Jizan Province -  جيزان'),
        ('tabuk', 'Tabuk Province -  تبوك'), ('bahah', 'Bahah Province -  الباحة'), ('najran', 'Najran Province -  نجران')])

    picture = FileField('Campaign Picture', validators=[FileAllowed(['jpg', 'png'])])    
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Add campaign')

    def validate_email(self, email):
        camp = Campaign.query.filter_by(email=email.data).first()
        if camp:
            raise ValidationError('Thats email is taken. please choose another one.!')

    def validate_name(self, name):
        name = name.data
        
        specials = ["!", "@", "#", "%", "^", "&", "*",  "-", "_", "=", "/", "+", "?", ".", ":", ";", "[", "]", ">", "<"]
        for n in name:
            for special in specials:
                if n == special:
                    raise ValidationError('This name has special chrachter')


class UpdateCampaignForm(FlaskForm):
    picture = FileField('Campaign Picture', validators=[FileAllowed(['jpg', 'png'])])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])
    lat = StringField('lat', validators=[DataRequired()])
    lng = StringField('lng', validators=[DataRequired()])

    needed_blood =SelectField('Blood Type / Priority', choices=[('o-', 'O-'), ('o+', 'O+'), ('a-', 'A-'), ('a+', 'A+'),
                                             ('b-', 'B-'), ('b+', 'B+'), ('ab-', 'AB-'), ('ab+', 'AB+')])
    city = SelectField('City', choices=[('riyadh', 'Riyadh Province -  الرياض'), ('jeddah', 'Jeddah Province -  جدة'),
     ('medinah', 'Medinah Province -  المدينة'), ('makkah', 'Makkah Province - مكة'), ('qassim', 'Qassim Province - القصيم'),
      ('easter', 'Easter Province - المنطقه الشرقيه'), ('asir', 'Asir Province -  عسير'), ('tabuk', 'Tabuk Province -  تبوك'),
       ('hail', 'Hail Province -  حايل'), ('northern', 'Norther Borders -  منطقة الحدود الشماليه'), ('jizan', 'Jizan Province -  جيزان'),
        ('tabuk', 'Tabuk Province -  تبوك'), ('bahah', 'Bahah Province -  الباحة'), ('najran', 'Najran Province -  نجران')])

    submit = SubmitField('Update campaign')    
          
        


class HospitalForm(FlaskForm):
    name = StringField('Hospital Name', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email' , validators=[DataRequired(), Email()])
    lat = StringField('lat', validators=[DataRequired()])
    lng = StringField('lng', validators=[DataRequired()])
    needed_blood =SelectField('Blood Type', choices=[('all', 'All'),('o-', 'O-'), ('o+', 'O+'), ('a-', 'A-'), ('a+', 'A+'),
                                             ('b-', 'B-'), ('b+', 'B+'), ('ab-', 'AB-'), ('ab+', 'AB+')])

    city = SelectField('City', choices=[('riyadh', 'Riyadh Province -  الرياض'), ('jeddah', 'Jeddah Province -  جدة'),
     ('medinah', 'Medinah Province -  المدينة'), ('makkah', 'Makkah Province - مكة'), ('qassim', 'Qassim Province - القصيم'),
      ('easter', 'Easter Province - المنطقه الشرقيه'), ('asir', 'Asir Province -  عسير'), ('tabuk', 'Tabuk Province -  تبوك'),
       ('hail', 'Hail Province -  حايل'), ('northern', 'Norther Borders -  منطقة الحدود الشماليه'), ('jizan', 'Jizan Province -  جيزان'),
        ('tabuk', 'Tabuk Province -  تبوك'), ('bahah', 'Bahah Province -  الباحة'), ('najran', 'Najran Province -  نجران')])

    picture = FileField('Hospital Picture', validators=[FileAllowed(['jpg', 'png'])])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Add Hospital')

    def validate_email(self, email):
        hosp = Hospital.query.filter_by(email=email.data).first()
        if hosp:
            raise ValidationError('Thats email is taken. please choose another one.!')

class UpdateHospitalForm(FlaskForm):
    needed_blood =SelectField('Blood Type', choices=[('all', 'All'),('o-', 'O-'), ('o+', 'O+'), ('a-', 'A-'), ('a+', 'A+'),
                                             ('b-', 'B-'), ('b+', 'B+'), ('ab-', 'AB-'), ('ab+', 'AB+')])
    
    picture = FileField('Hospital Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Hospital')






class SearchCampHosp(FlaskForm):
    choose = SelectField('Choose', choices=[('hospital', 'Hospital'), ('campaign' , 'Campaign')])
    city = SelectField('City', choices=[('riyadh', 'Riyadh Province -  الرياض'), ('jeddah', 'Jeddah Province -  جدة'),
     ('medinah', 'Medinah Province -  المدينة'), ('makkah', 'Makkah Province - مكة'), ('qassim', 'Qassim Province - القصيم'),
      ('easter', 'Easter Province - المنطقه الشرقيه'), ('asir', 'Asir Province -  عسير'), ('tabuk', 'Tabuk Province -  تبوك'),
       ('hail', 'Hail Province -  حايل'), ('northern', 'Norther Borders -  منطقة الحدود الشماليه'), ('jizan', 'Jizan Province -  جيزان'),
        ('tabuk', 'Tabuk Province -  تبوك'), ('bahah', 'Bahah Province -  الباحة'), ('najran', 'Najran Province -  نجران')])

    submit = SubmitField('Search')


class CommentForm(FlaskForm):
    comment = StringField("Your Comment")
    submit = SubmitField('Comment')



