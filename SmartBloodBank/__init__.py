from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_googlemaps import GoogleMaps
from SmartBloodBank.config import Config








db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
GoogleMaps = GoogleMaps()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app) 
    login_manager.init_app(app) 

    GoogleMaps.init_app(app)


    app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT =465,
    MAIL_USE_SSL =True,
    MAIL_USERNAME = 'shuwaier.a@gmail.com',
    MAIL_PASSWORD = 'abdullaH051777'
    )

    mail.init_app(app)

    from SmartBloodBank.users.routes import users
    from SmartBloodBank.campaigns.routes import camp
    from SmartBloodBank.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(camp)
    app.register_blueprint(main)

    return app
