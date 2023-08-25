from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'

    db.init_app(app)
    
    from .auth import auth
    from .views import views
    
    from .message import message
  
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/auth')
   
    app.register_blueprint(message, url_prefix='/message')
  
    
    with app.app_context():
        db.create_all()

    login_manager.login_view = 'auth.signin'  # Set login view before initializing LoginManager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    return app
