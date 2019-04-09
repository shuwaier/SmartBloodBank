import secrets
import os
from PIL import Image
from flask import  render_template, url_for, flash, redirect, request, abort, Blueprint, current_app, jsonify
from SmartBloodBank import create_app, db, bcrypt, mail
from SmartBloodBank.models import User, Donor, Campaign, Hospital, UserComment
from SmartBloodBank.campaigns.forms import (CampaignForm, HospitalForm, SearchCampHosp, UpdateCampaignForm, UpdateHospitalForm, CommentForm)
from SmartBloodBank.campaigns.utils import save_pic
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from datetime import datetime
from urllib.request import Request, urlopen

camp = Blueprint('camp', __name__)




@camp.route("/add_campaign",  methods=['GET', 'POST'])
@login_required
def add_campaign():
        if current_user.us_type == 1 or current_user.us_type == 0:
          form = CampaignForm()

          if form.validate_on_submit():
               if form.picture.data:
                    picture_file = save_pic(form.picture.data)
                    camp = Campaign(name=form.name.data, email=form.email.data,
                         image_file=picture_file, needed_blood=form.needed_blood.data, lat=form.lat.data, lng=form.lng.data, phone=form.phone.data, city=form.city.data, leader=current_user)
               else:
                    camp = Campaign(name=form.name.data, email=form.email.data,
                              needed_blood=form.needed_blood.data, lat=form.lat.data, lng=form.lng.data, phone=form.phone.data, city=form.city.data, leader=current_user)
               db.session.add(camp)
               db.session.commit()
               flash('Your Campaign is added sucessfully', 'success')
               return redirect(url_for('main.home'))   
          return render_template('add_campaign.html', title='Add Campaign', form=form )
        else:
             flash('You are not authoraized to add campaign', 'danger')
             return redirect(url_for('main.home'))




@camp.route("/add_hospital", methods=['GET', 'POST'])
@login_required
def add_hospital():
     if current_user.us_type == 0:
          form = HospitalForm()
          if form.validate_on_submit():
               if form.picture.data:
                    picture_file = save_pic(form.picture.data)
                    hosp = Hospital(name=form.name.data, email=form.email.data, lat=form.lat.data, lng=form.lng.data,
                               image_file=picture_file, phone=form.phone.data, needed_blood=form.needed_blood.data, city=form.city.data ,leaderAdmin=current_user)
               else:
                    hosp = Hospital(name=form.name.data, email=form.email.data, lat=form.lat.data, lng=form.lng.data,
                               phone=form.phone.data, needed_blood=form.needed_blood.data, city=form.city.data ,leaderAdmin=current_user)
               db.session.add(hosp)
               db.session.commit()
               flash('Your Hospital is added sucessfully', 'success')
               return redirect(url_for('main.home'))
          return render_template('add_hospital.html', title='Add Hospital', form=form)
     else:
           flash('You are not authoraized to add hospital', 'danger')
           return redirect(url_for('main.home'))




@camp.route('/edit_camp/<int:campId>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campId):
     campId = int(campId)
     camp = Campaign.query.get_or_404(campId)
     if current_user.us_type == 0:
          pass
     elif camp.leader != current_user:
          abort(403)
     form = UpdateCampaignForm()
     if form.validate_on_submit():
          if form.picture.data:
               picture_file = save_pic(form.picture.data)
               camp.image_file = picture_file
          camp.lat = form.lat.data
          camp.lng = form.lng.data
          camp.needed_blood = form.needed_blood.data
          camp.phone = form.phone.data
          camp.city = form.city.data
          db.session.commit()
          flash('Your Campaign has been updated! successfully', 'success')
          return redirect(url_for('users.update_account'))
     elif request.method == 'GET':
          form.lng.data = camp.lng
          form.lat.data = camp.lat
          form.needed_blood.data = camp.needed_blood
          form.phone.data = camp.phone
          form.city.data = camp.city
     return render_template('update_campaign.html', title='Update Campaign', form=form)


@camp.route('/edit_hosp/<int:hospId>', methods=['GET', 'POST'])
@login_required
def edit_hospital(hospId):
     hosp = Hospital.query.get_or_404(hospId)
     if current_user.us_type != 0:
          abort(403)
     form = UpdateHospitalForm()
     if form.validate_on_submit():
          if form.picture.data:
               picture_file = save_pic(form.picture.data)
               hosp.image_file = picture_file
          hosp.needed_blood = form.needed_blood.data
          db.session.commit()
          flash('The hospital has been updated successfully!', 'success')
          return redirect(url_for('main.home'))
     elif request.method == 'GET':
          form.needed_blood.data = hosp.needed_blood
     return render_template('update_hospital.html', title='Update Hospital', form=form)




@camp.route("/search", methods=['GET', 'POST'])
def search():
     form = SearchCampHosp()
     if form.validate_on_submit:
           if form.choose.data == 'hospital':
                hosps = Hospital.query.filter_by(city=form.city.data).first()
                if hosps:
                    hosps = Hospital.query.filter_by(city=form.city.data) 
                    return render_template('hospital.html', hosps=hosps)
                else:
                    flash('Sorry, There is no Hospitals in ' + form.city.data.capitalize()  , 'warning')
                    return redirect(url_for('camp.search'))
           elif form.choose.data == 'campaign':
               camps = Campaign.query.filter_by(city=form.city.data).first()
               if camps:
                    camps = Campaign.query.filter_by(city=form.city.data)
                    return render_template('campaign.html', camps=camps)
               else:
                    flash('Sorry, There is no campaigns in ' + form.city.data.capitalize()  , 'warning')
                    return redirect(url_for('camp.search'))
     
     return render_template('search_camp_hospital.html', title='Search', form=form)


@camp.route("/camp_detail/<int:campId>", methods=['GET', 'POST'])
def camp_detail(campId):
     camp = Campaign.query.get_or_404(campId)
     comments = UserComment.query.filter_by(Campaign=campId)
     form = CommentForm()
     if form.validate_on_submit():
          comment = UserComment(user_id=current_user.id, Campaign=campId, comment=form.comment.data)
          db.session.add(comment)
          db.session.commit()
     return render_template('camp.html', title=camp.name, camp=camp, form=form, comments=comments)




@camp.route("/campaign")
def campaign():
     camps = Campaign.query.all()
     return render_template('campaign.html', camps=camps)


@camp.route("/campaign/map_camp/<int:campId>")
def campaign_location(campId):
     camp = Campaign.query.get_or_404(campId)
     lat = jsonify(camp.lat)
     lng = jsonify(camp.lng) 
     return render_template('map_camp.html', lat=lat, lng=lng)


@camp.route("/hospital")
def hospital():
     hosps = Hospital.query.all()
     return render_template('hospital.html', hosps=hosps)



@camp.route("/edited_hospital")
@login_required
def edited_hospital():
     if current_user.us_type == 0:
          hosps = Hospital.query.all()
          return render_template('edited_hospital.html', title='Hospitals', hosps=hosps)
     flash('Your not authoraized')
     return redirect(url_for('main.home'))




