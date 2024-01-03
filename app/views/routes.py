from flask import render_template, request, flash, jsonify
from . import views
from ..db import find_patient_app, find_rev, find_doctor_app, find_doc, find_patient
from flask_login import current_user, login_required
from app.models import Doctor

@views.route('/')
def index():
    return render_template('base.html')

@views.route('/profile/patient', methods=['GET'])
@login_required
def patient_profile():
    """ Renders the profile page once patient is logged in """
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
@login_required
def doctor_profile():
    """ Renders the profile page once doctor is logged in """
    appointments = find_doctor_app(current_user.id)
    reviews = []
    for appointment in appointments:
        review_info = {
            'review': find_rev(appointment.id),
            'patient': find_patient(appointment.id)
        }
        reviews.append(review_info)
    return render_template('doctor_profile.html', current_user=current_user, apps=appointments, revs=reviews)

@views.route('/display/<int:id>')
def display(id):
    return render_template('display.html')

@views.route('/api/doctors', methods=['GET'])
@login_required
def api_get_doctors():
    """ API endpoint to fetch doctors based on specialty """
    specialty = request.args.get('specialty')
    if specialty:
        doctors = Doctor.query.filter_by(specialization=specialty).all()
    else:
        doctors = Doctor.query.all()

    doctor_data = [{
        "id": doctor.id,
        "name": f"{doctor.first_name} {doctor.last_name}",
        "specialization": doctor.specialization, 
        "profile_picture_url": doctor.profile_picture_url, 
        "bio": doctor.bio,
        "location": doctor.location, 
        "contact": doctor.contact
    } for doctor in doctors]

    return jsonify(doctor_data)

@views.route('/find-doctors')
def find_doctors():
    """ Renders a page with doctors based on the selected specialty """
    specialty = request.args.get('specialty', '')
    doctors = Doctor.query.filter_by(specialization=specialty).all() if specialty else []
    return render_template('find_doctors.html', doctors=doctors)
