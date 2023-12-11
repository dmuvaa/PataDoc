from flask import Flask
from .models import db
from .views.routes import main
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User, UserData, Doctor, Specialization, DoctorSpecialization, Appointment, Review

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .auth import auth as auth_blueprint

    app.register_blueprint(main)

    # Import and register other blueprints (auth, user, doctor)

    return app
