""" Module handles sign up and login routes """
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..db import register_user, find_user_by, hash_password
from flask_login import login_user, current_user
from . import auth

@auth.route('/sign-up', methods=['GET', 'POST'], strict_slashes=False)
def sign_up():
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

        if first_name is None:
            flash('email missing', category='error')
        if password is None:
            flash('password missing', category='error')
        if first_name is None:
            flash('FirstName missing', category='error')
        if last_name is None:
            flash('LastName missing', category='error')
        try:
            register_user(first_name, last_name, email, contact_number, password)
            return redirect(url_for('auth.login'))
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
            flash(error_msg, category='error')
                
    return render_template('sign_up.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ Logins in the user """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = find_user_by(email)
            print("{}".format(user))
            print("{}".format(user.password_hash))
            if (hash_password(password) == user.password_hash):
                login_user(user, remember=True)
                print("Success")
                flash('Logged in successfully!', category='success')               
                return redirect(url_for('views.routes.profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        except Exception as e:
            error_msg = "User does not exist."
            flash(error_msg, category='error')
    return render_template("login.html", user=current_user)
