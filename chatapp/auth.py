from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify,Flask
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url
import cloudinary
import os






auth = Blueprint('auth', __name__)

app = Flask(__name__)

@auth.route('/')
def base():
    return render_template("base.html")

@auth.route('/home', methods=['GET', 'POST'])
@login_required  # Add the login_required decorator here
def home():
    return render_template("chat.html")

@auth.route('/chatUser', methods=['GET'])
@login_required
def chatUser():
    return render_template('chat_with_admin.html')


@auth.route('/profile', methods=['GET'])
@login_required  # Add the login_required decorator here
def profile():
    user = current_user 
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        about = request.form['about']
        profile_picture = request.files['profile_picture']
        flash('Profiles Updated SucessFully', category='error')

        if profile_picture:
            # Upload image to Cloudinary
            upload_result = upload(profile_picture)
            profile_picture_url, options = cloudinary_url(upload_result['public_id'], format="jpg") 
    return render_template("profile.html", user=user)

cloudinary.config( 
  cloud_name = "dwxmvddcd", 
  api_key = "485855482193362", 
  api_secret = "***************************" 
)



############# ROUTE FOR SIGN IN ############
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter_by(phone=phone).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)

                return redirect(url_for('auth.home'))  # Redirect to user's dashboard

        else:
            flash("User not found or not registered", category='error')

    return render_template("existingUser.html")

#############  END OF ROUTE FOR SIGN IN ############



############# ROUTE FOR SIGN OUT ############
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", category='success')
    return redirect(url_for('auth.base'))

############# END OF  ROUTE FOR SIGN OUT ############




########### ROUTE FOR SIGN UP #############

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')  # Corrected
        address = request.form.get('address')

        if len(address) < 2:
            flash('Valid address is required.', category='error')
        elif len(phone) < 11:
            flash('Check your phone number.', category='error')
        elif len(name) < 2:
            flash('Name is required.', category='error')
        elif password1 != password2:  # Corrected
            flash('Passwords do not match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least eight characters long.', category="error")
        else:
            new_user = User(name=name, phone=phone, address=address,
                            password=generate_password_hash(password1, method='sha256'))

            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!', category="success")
            return redirect(url_for('auth.login'))
    return render_template('newUser.html', user=current_user)

    
    ################ END OF SIGN UP ROUTE ###################
        
  



############## SEARCHES #############
@auth.route('/search_users', methods=['GET'])
@login_required
def search_users():
    term = request.args.get('term')
    users = User.query.filter(User.name.ilike(f'%{term}%')).all()
    user_list = [{"name": user.name} for user in users]
    return jsonify(users=user_list)
######## END OF SEARCHES #################







