from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()
UPLOAD_FOLDER = 'static/uploads/'


def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_ADMIN_SIGNUPS'] = 3

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    from .models import User, Doctor, Admin, Specialization, DoctorSpecialization, Appointment, Review

    @app.before_request
    def before_request():
        g.admin_signup_counter = 0

    @login_manager.user_loader
    def load_user(user_id):
        user_type = session.get('user_type', 'user')

        if user_type == 'user':
            return User.query.get(int(user_id))
        elif user_type == 'doctor':
            return Doctor.query.get(int(user_id))
        elif user_type == 'admin':
            return Admin.query.get(int(user_id))
        else:
            return None
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)

    @app.teardown_appcontext
    def teardown_db(exception=None):
        db.session.remove()

    return app