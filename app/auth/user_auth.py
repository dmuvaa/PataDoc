""" Module handles sign up and login routes """
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..db import register_user

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


@auth.route('/login')
def login():
    return render_template('login.html')