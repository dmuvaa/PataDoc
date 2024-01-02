""" Module handles sign up and login routes """
from flask import render_template, request, flash, redirect, url_for, session, current_app
from ..db import *
from flask_login import login_user, current_user, login_required

from . import auth
from werkzeug.security import check_password_hash

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    """ Checks whether the image file type is among the allowed extentions """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/sign-up/doctor', methods=['GET', 'POST'], strict_slashes=False)
def sign_up_doc():
    """ sign up method """

    data = None
    if request.method == 'POST':
        try:
            data = request.form
        except Exception as e:
            flash('Wrong format', category='error')
            
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        contact = data.get('contact')        
        password = data.get('password')
        speciality = data.get('speciality')
        bio = data.get('bio')
        license_no = data.get('license_no')

        try:
            register_doc(
                first_name, last_name, email, contact, password, speciality,
                bio, license_no)
            flash('Sign up successful!', category='success')
            return redirect(url_for('auth.login_doc'))
        except Exception as e:
            error_msg = "Can't create Doctor profile: {}".format(e)
            flash(error_msg, category='error')       
    return render_template('doc_signup.html')


@auth.route('/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture(user_type=None):
    print(f'Session in upload_profile_picture: {session}')
    if 'image' in request.files:
        image = request.files['image']
        user_type = request.form.get('user_type')
        print(f'Session in upload_profile_picture: {user_type}')
        
        if image and allowed_file(image.filename):
            try:
                if user_type == 'user':
                    save_patient_profile(current_user.id, image)
                elif user_type == 'doctor':
                    save_doctor_profile(current_user.id, image)
                else:
                    raise ValueError("Invalid user type")

                flash('Profile picture uploaded successfully!', category='success')
            except Exception as e:
                error_msg = f"Could not upload profile picture: {e}"
                flash(error_msg, category='error')
        else:
            flash('Image format is invalid!', category='error')

    return redirect(url_for('views.doctor_profile'))



@auth.route('/login/doctor', methods=['GET', 'POST'])
def login_doc():
    """ Logins in the user """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            doctor = find_doc_by(email)

            if doctor and check_password_hash(doctor.password_hash, password):
                session['user_type'] = 'doctor'
                doctor.user_type = 'doctor'
                login_user(doctor, remember=True)
                flash('Logged in successfully!', category='success')
                print(f'Session in login_doc: {session}')

                return redirect(url_for('views.doctor_profile'))
            else:
                flash('Incorrect email or password, try again.', category='error')
        except Exception as e:
            # error_msg = "An error occurred during login."
            # flash(error_msg, category='error')
            print(e)
    return render_template("login.html", doctor=current_user)
