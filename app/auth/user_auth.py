""" Module handles sign up and login routes """
from flask import render_template, request, flash, redirect, url_for, session
from ..db import register_user, find_user_by
from flask_login import login_user, current_user, login_required, logout_user
from . import auth
from werkzeug.security import check_password_hash


@auth.route('/sign-up/patient', methods=['GET', 'POST'], strict_slashes=False)
def sign_up_patient():
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
        contact_number = data.get('contact')        
        password = data.get('password')

        if email is None:
            flash('email missing', category='error')
        if password is None:
            flash('password missing', category='error')
        if first_name is None:
            flash('FirstName missing', category='error')
        if last_name is None:
            flash('LastName missing', category='error')
        try:
            register_user(first_name, last_name, email, contact_number, password)
            return redirect(url_for('auth.login_patient'))
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
            flash(error_msg, category='error')
                
    return render_template('sign_up.html')


@auth.route('/login/patient', methods=['GET', 'POST'])
def login_patient():
    """ Logins in the user """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = find_user_by(email)
            if user and check_password_hash(user.password_hash, password):
                session['user_type'] = 'user'
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.patient_profile'))
            else:
                flash('Incorrect email or password, try again.', category='error')
        except Exception as e:
            # error_msg = "An error occurred during login."
            # flash(error_msg, category='error')
            print(e)
    return render_template("login.html", user=current_user)

