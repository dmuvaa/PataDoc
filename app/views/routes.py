from flask import render_template, request, flash
from . import views
from ..db import find_patient_app, find_rev, find_doctor_app, find_doc, find_patient
from flask_login import current_user, login_required, logout_user


@views.route('/')
def index():
    return render_template('base.html')

@views.route('/profile/patient', methods=['GET'])
def patient_profile():
    """ Renders the profile page once patient is logged in"""
    appointments = find_patient_app(current_user.id)
    reviews = []
    for appointment in appointments:
        review_info = {
            'review': find_rev(appointment.id),
            'doctor': find_doc(appointment.id)
        }
        reviews.append(review_info)
    return render_template('patient_profile.html', apps=appointments, revs=reviews)

@views.route('/profile/doctor', methods=['GET'])
def doctor_profile():
    """ Renders the profile page once doctor is logged in"""
    appointments = find_doctor_app(current_user.id)
    reviews = []
    for appointment in appointments:
        review_info = {
            'review': find_rev(appointment.id),
            'patient': find_patient(appointment.id)
        }
        reviews.append(review_info)
    return render_template('patient_profile.html', apps=appointments, revs=reviews)

@views.route('/display/<int:id>')
def display(id):
    return render_template('display.html')