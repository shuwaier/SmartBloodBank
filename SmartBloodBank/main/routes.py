from flask import  render_template ,Blueprint
from flask_googlemaps import Map
from urllib.request import Request, urlopen

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():


      return render_template('home.html', title='Home')

