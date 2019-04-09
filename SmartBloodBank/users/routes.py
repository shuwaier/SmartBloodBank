
import secrets
import os
from PIL import Image
from flask import  render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from SmartBloodBank import db, bcrypt, mail
from SmartBloodBank.models import User, Donor, Campaign, Hospital
from SmartBloodBank.users.forms import (DonorRegistrationForm, LeaderRegistrationForm, LoginForm, UpdateAccountForm,
  InviteForm, ConfirmDonation, RequestBloodForm)
from SmartBloodBank.users.utils import save_pic
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from datetime import datetime


users = Blueprint('users', __name__)


@users.route("/donor_register", methods=['GET', 'POST'])
def donor_register():
     form = DonorRegistrationForm()
     if form.validate_on_submit():
          city1 = form.city.data
          hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
          if form.picture.data:
               picture_file = save_pic(form.picture.data)
               user = User(username=form.username.data, email=form.email.data, phone=form.phone.data,
                           city=form.city.data,
                           image_file=picture_file, password=hashed_password, first_name=form.first_name.data,
                           last_name=form.last_name.data, us_type=2)
               donor = Donor(user_id=user.id, blood_type=form.blood_type.data, city=city1, donor=user)
          else:
               user = User(username=form.username.data, email=form.email.data, phone=form.phone.data,
                           city=form.city.data,
                           password=hashed_password, first_name=form.first_name.data, last_name=form.last_name.data,
                           us_type=2)
               donor = Donor(user_id=user.id, city=city1, blood_type=form.blood_type.data, donor=user)

          db.session.add(user)
          db.session.add(donor)
          db.session.commit()
          donor = Donor(user_id=user.id, blood_type=form.blood_type.data, donor=user)
          flash('Your account has been created! You are now able to login', 'success')
          return redirect(url_for('main.home'))
     return render_template('donor_register.html', form=form, title='Donor Register')


@users.route("/leader_register",  methods=['GET', 'POST'])
def leader_register():
     form = LeaderRegistrationForm()
     if form.validate_on_submit():
          hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
          if form.picture.data:
               picture_file = save_pic(form.picture.data)
               user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, city=form.username.data,
                    image_file=picture_file, password=hashed_password,first_name=form.first_name.data,last_name=form.last_name.data, us_type=0)
          else:
               user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, city=form.username.data,
                    password=hashed_password,first_name=form.first_name.data,last_name=form.last_name.data, us_type=0)
          db.session.add(user)
          db.session.commit()
          flash('Your account has been created! You are now able to login', 'success')
          return redirect(url_for('main.home'))
     return render_template('leader_register.html', form=form, title='Leader Register')




@users.route("/login", methods=['GET', 'POST'])
def login():
     if current_user.is_authenticated:
        return redirect(url_for('main.home'))
     form = LoginForm()
     if form.validate_on_submit():
          user = User.query.filter_by(email=form.email.data).first()
          if user and bcrypt.check_password_hash(user.password, form.password.data):
             login_user(user)
             return  redirect(url_for('main.home'))
          else:
            flash('Unesuccessful. Please check email and password' ,'danger')
     return render_template('login.html', title='login', form=form)


@users.route("/logout")
def logout():    
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/update_account",  methods=['GET', 'POST'])
@login_required
def update_account():
     form = UpdateAccountForm()
     if form.validate_on_submit():
          current_user.city = form.city.data
          current_user.phone = form.phone.data
          current_user.first_name = form.first_name.data
          current_user.last_name = form.last_name.data
          db.session.commit()
          flash('Your account has been updated' , 'success')
          return redirect(url_for('users.update_account'))
     elif request.method == 'GET':
          form.phone.data = current_user.phone
          form.city.data = current_user.city
          form.first_name.data = current_user.first_name
          form.last_name.data = current_user.last_name
     return render_template('update_account.html', title='Update Account', form=form)




@users.route("/my_campaign")
@login_required
def my_campaign():
     if current_user.us_type == 1:
          camps =  Campaign.query.filter_by(user_id = current_user.id)
          return render_template('my_campaign.html', title='My Camaign', camps=camps)
     elif current_user.us_type == 0:
          camps = Campaign.query.all()
          return render_template('my_campaign.html', title='My Camaign', camps=camps)
     flash('Your not authorized')
     return redirect(url_for('main.home'))



@users.route("/invite_friend", methods=['GET', 'POST'])
@login_required
def invite_friend():
     if current_user.us_type != 2:
          flash('Your not authorized to invite your friend', 'warning')
          return redirect(url_for('main.home'))
     else:
          form = InviteForm()
          if form.validate_on_submit():
               msg = Message('Addres',
                              sender='Smart Blood Bank',
                              recipients=[form.email.data])
                              
                              
               msg.body = f''' Your Friend has invited you to come and donate, visit to get more information
               https://www.google.com
                              '''
               mail.send(msg)
               return redirect(url_for('main.home'))
          return render_template('invite_friend.html', title='Invite Friend', form=form)




@users.route("/confirm_donation", methods=['GET', 'POST'])
@login_required
def confirm_donation():
     if current_user.us_type != 1:
          flash('Your not authorized to invite your friend', 'warning')
          return redirect(url_for('main.home'))
     elif current_user.us_type == 1:
          form = ConfirmDonation()
          if form.validate_on_submit():
               user = User.query.filter_by(email=form.email.data).first()
               if user:
                    user.donor.score +=1
                    user.donor.last_donation = datetime.now()
                    db.session.commit()
                    flash('The score and last donation for the donor has been updated', 'info')
                    return redirect(url_for('main.home'))
          return render_template('confirm_donation.html', title='Confirm Donation', form=form)


@users.route("/request_blood/search", methods=['GET', 'POST'])
@login_required
def request_blood_serach():
     form = RequestBloodForm()
     if form.validate_on_submit():
          city = form.city.data
          blood_type = form.blood_type.data
          message = form.comment.data
          return redirect(url_for('users.request_blood_select', city1=city, blood_type1=blood_type,message1=message ))
     return render_template('request_blood_search.html', title="Request Blood", form=form)



@users.route("/request_blood/select/<city1>/<blood_type1>/<message1>", methods=['GET', 'POST'])
@login_required
def request_blood_select(city1,blood_type1,message1):
     donors = Donor.query.filter_by(city=city1, blood_type=blood_type1)
     for donor1 in donors:
          email = donor1.donor.email
          name = donor1.donor.first_name
          msg = Message('Addres',
                         sender='Smart Blood Bank',
                         recipients=[email])

          msg.body = f''' Hello {name} there is someone  requesting you to donate based on your blood type and city
               and this is the message
                --{message1}--
               {url_for('main.home', _external=True)}
                               '''

          mail.send(msg)
     return redirect(url_for('main.home'))



@users.route("/leader/<int:userId>", methods=['GET', 'POST'])
def leader(userId):
     user = User.query.filter_by(id=userId).first()
     camps = Campaign.query.filter_by(user_id=userId)
     return render_template('leader.html', title='Leader', user=user, camps=camps)


