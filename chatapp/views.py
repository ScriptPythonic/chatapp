from flask import Blueprint,render_template,Flask,request,flash,url_for,redirect,jsonify

from . import db
from flask_login import LoginManager
from flask_login import login_user, login_required


app = Flask(__name__)
#adding blueprint 
views = Blueprint('views', __name__)

@views.route('/')
def base():
    
    return render_template("base.html")




