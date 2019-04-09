import secrets
import os
from PIL import Image
from flask import  render_template, url_for, flash, redirect, request, abort, current_app
from SmartBloodBank import db, bcrypt, mail
from SmartBloodBank.models import User, Donor, Campaign, Hospital
from SmartBloodBank.forms import (DonorRegistrationForm, LeaderRegistrationForm, LoginForm, UpdateAccountForm,
 CampaignForm, HospitalForm, InviteForm, ConfirmDonation, SearchCampHosp, UpdateCampaignForm, UpdateHospitalForm)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from datetime import datetime


     










































