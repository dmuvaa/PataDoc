""" Module handles sign up and login routes """
from flask import render_template, request, flash, redirect, url_for
from ..db import register_doc, find_doc_by
from flask_login import login_user, current_user
from . import auth
from werkzeug.security import check_password_hash

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
        bio = data.get('bio')
        profile_picture_url = data.get('profile_picture_url')
        license_no = data.get('license_no')

        # if first_name is None:
        #     flash('email missing', category='error')
        # if password is None:
        #     flash('password missing', category='error')
        # if first_name is None:
        #     flash('FirstName missing', category='error')
        # if last_name is None:
        #     flash('LastName missing', category='error')
        try:
            register_doc(
                first_name, last_name, email, contact, password, bio,
                profile_picture_url, license_no)
            return redirect(url_for('auth.login_doc'))
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
            flash(error_msg, category='error')
                
    return render_template('doc_signup.html')

@auth.route('/login/doctor', methods=['GET', 'POST'])
def login_doc():
    """ Logins in the user """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = find_doc_by(email)
            if user and check_password_hash(user.password_hash, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.doctor_profile'))
            else:
                flash('Incorrect email or password, try again.', category='error')
        except Exception as e:
            # error_msg = "An error occurred during login."
            # flash(error_msg, category='error')
            print(e)
    return render_template("login.html", user=current_user)
