import os
import secrets
from PIL import Image
from flask import url_for, current_app,request
from flask_mail import Message
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map



def save_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # resizng img 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    return picture_fn


