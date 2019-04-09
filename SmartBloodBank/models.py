from flask_login import UserMixin
from SmartBloodBank import db, login_manager
from datetime import datetime
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return  User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)   
    password = db.Column(db.String(16), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    us_type = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(10), nullable=True)
    donor = db.relationship('Donor', uselist=False , backref='donor')
    campaigns = db.relationship('Campaign', backref='leader', lazy=True)
    hospital = db.relationship('Hospital', backref='leaderAdmin', lazy=True)
    comment = db.relationship('UserComment', backref='commentUser', lazy=True)
    


    

    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)   
    lat = db.Column(db.String(250), nullable=False)
    lng = db.Column(db.String(250), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='campaign.jpg')
    city = db.Column(db.String(100), nullable=False)
    needed_blood = db.Column(db.String(3), nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)





class Comment(db.Model):
    text = db.Column(db.String(250), nullable=False)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    camp_id = db.Column(db.Integer, nullable=False)






class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)   
    lat = db.Column(db.String(250), nullable=False)
    lng = db.Column(db.String(250), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='hospital.jpg')
    city = db.Column(db.String(100), nullable=False)
    needed_blood = db.Column(db.String(3), nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Hospital('{self.name}', '{self.user_id}')"


class  Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blood_type = db.Column(db.String(3), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=True, default=0)
    last_donation = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Donor('{self.blood_type}')"





class City(db.Model):
    Id = db.Column(db.Integer, primary_key=True, nullable=False)
    cityNameAR = db.Column(db.String(100))
    cityNameEnd = db.Column(db.String(100))

    def __repr__(self):
        return f"City( '{self.Id}' ,'{self.cityNameAR}')"




class UserComment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.String(1000), nullable=False)
    Campaign = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

    def __repr__(self):
        return f"UserComment('{self.comment}')"