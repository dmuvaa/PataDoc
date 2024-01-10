""" Module handles sign up and login routes """
from flask import render_template, request, flash, redirect, url_for, session, g, current_app
from ..db import register_admin, find_admin_by
from flask_login import login_user, current_user
from . import auth
from werkzeug.security import check_password_hash


@auth.route('/sign-up/admin', methods=['GET', 'POST'], strict_slashes=False)
def sign_up_admin():
    """ sign up method """
    if g.admin_signup_counter >= current_app.config['MAX_ADMIN_SIGNUPS']:
        flash('Maximum number of admin sign-ups reached.', 'error')
        return redirect(url_for('index'))
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
            g.admin_signup_counter += 1
            register_admin(first_name, last_name, email, contact_number, password)
            flash('Admin sign-up successful.', 'success')
            return redirect(url_for('auth.login_admin'))

        except Exception as e:
            error_msg = "Can't create Admin: {}".format(e)
            flash(error_msg, category='error')
                
    return render_template('admin_signup.html')


@auth.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    """ Logins an admin """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            admin = find_admin_by(email)
            if admin and check_password_hash(admin.password_hash, password):
                session['user_type'] = 'admin'
                login_user(admin, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.view_pending_doctors'))
            else:
                flash('Incorrect email or password, try again.', category='error')
        except Exception as e:
            # error_msg = "An error occurred during login."
            # flash(error_msg, category='error')
            print(e)
    return render_template("login.html", admin=current_user)

