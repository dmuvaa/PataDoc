from flask import render_template, request, flash, redirect, url_for
from . import views
from ..db import find_patient_app, find_rev, find_doctor_app, find_doc, find_patient
from flask_login import current_user, login_required
import requests
from ..models import Doctor
from exchangelib import Credentials, Account, DELEGATE, HTMLBody, Message
from .. import db
import os


@views.route('/')
def index():
    return render_template('base.html')

@views.route('/profile/patient', methods=['GET'])
@login_required
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

    # api_url = 'https://api.calendly.com/scheduled_events'
    # headers = {'Authorization': f'Bearer '}

    # response = requests.get(api_url, headers=headers)
    # response.raise_for_status()
    # appointments= response.json()
    return render_template('patient_profile.html', apps=appointments, revs=reviews)

@views.route('/profile/doctor', methods=['GET'])
@login_required
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
    return render_template('doctor_profile.html', current_user=current_user, apps=appointments, revs=reviews)

@views.route('/admin/pending_doctors')
# @login_required  # Ensure only admin can access
def view_pending_doctors():
    pending_doctors = Doctor.query.filter_by(approved=False).all()
    return render_template('pending_doctors.html', pending_doctors=pending_doctors)

@views.route('/admin/approve_doctor/<int:doctor_id>', methods=['POST'])
# @login_required  # Ensure only admin can access
def approve_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.approved = True

    # Replace these values with your Outlook account details
    email_address = os.getenv('EMAIL')
    password = os.getenv('password')
    recipient_email = doctor.email
    subject = 'Approval Successful'
    body = 'Congratulations! Your registration has been approved successfully.'

    # Set up credentials
    credentials = Credentials(email_address, password)

    # Connect to the Outlook account
    account = Account(email_address, credentials=credentials, autodiscover=True, access_type=DELEGATE)

    # Create an email message
    email = Message(
        account=account,
        subject=subject,
        body=HTMLBody(body),
        to_recipients=[recipient_email]
    )

    # Send the email
    email.send()


    # Commit changes to the database
    db.session.commit()

    flash('Doctor approved successfully.', 'success')
    return redirect(url_for('views.view_pending_doctors'))

@views.route('/admin/decline_doctor/<int:doctor_id>', methods=['POST'])
# @login_required  # Ensure only admin can access
def decline_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)

    # Replace these values with your Outlook account details
    email_address = 'patadoc@outlook.com'
    password = '3Engineers'
    recipient_email = doctor.email
    subject = 'Approval Declined'
    body = 'We regret to inform you that your registration has been declined.'

    # Set up credentials
    credentials = Credentials(email_address, password)

    # Connect to the Outlook account
    account = Account(email_address, credentials=credentials, autodiscover=True, access_type=DELEGATE)

    # Create an email message
    email = Message(
        account=account,
        subject=subject,
        body=HTMLBody(body),
        to_recipients=[recipient_email]
    )

    # Send the email
    email.send()

    # Delete the doctor from the database
    db.session.delete(doctor)

    # Commit changes to the database
    db.session.commit()

    flash('Doctor declined and deleted successfully.', 'success')
    return redirect(url_for('admin.view_pending_doctors'))


@views.route('/appointment/')

@views.route('/display/<int:id>')
def display(id):
    return render_template('display.html')