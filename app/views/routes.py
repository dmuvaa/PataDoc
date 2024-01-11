from flask import render_template, request, flash, redirect, url_for, session, jsonify
from . import views
import os
from ..db import *
from flask_login import current_user, login_required
from app.models import Doctor
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
import requests
from ..models import Doctor
from exchangelib import Credentials, Account, DELEGATE, HTMLBody, Message
from .. import db
import os
from functools import wraps
from dotenv import load_dotenv

def allowed_file(filename):
    """ Checks whether the image file type is among the allowed extentions """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))  # Redirect to a non-admin page
    return decorated_function

@views.route('/')
def index():
    return render_template('home.html')

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
    return render_template('patient_profile.html', apps=appointments, current_user=current_user, revs=reviews, user_id=str(current_user.id),
                        image_exists=os.path.exists(f'app/static/user_profile/{current_user.id}.jpg'))

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
    return render_template('doctor_profile.html', current_user=current_user, apps=appointments,
                           revs=reviews, user_id=str(current_user.id),
                           image_exists=os.path.exists(f'app/static/doctor_profile/{current_user.id}.jpg'))

@views.route('/leave-review/<int:doctor_id>/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def leave_review(doctor_id, appointment_id):
    """ User leaves a review"""

    if not valid_review(doctor_id, appointment_id):
        flash('Invalid doctor or appointment.', 'error')
        return redirect(url_for('views.index'))

    if request.method == 'POST':
        rating = float(request.form.get('rating'))
        comment = request.form.get('comment')

        appointment = valid_review(doctor_id, appointment_id)
        doctor = find_doctor_app(doctor_id)
        try:
            save_review(appointment, rating, comment)
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('views.index'))
        except Exception as e:
            flash('Could not submit review!', 'error')
            return redirect(url_for('views.index'))

    return render_template('leave_review.html', doctor=doctor, appointment=appointment)

@views.route('/upload-user-picture', methods=['POST'])
@login_required
def upload_user_picture():
    """ Uploads user's profile picture"""
    if 'image' in request.files:
        image = request.files['image']
        
        if image and allowed_file(image.filename):
            try:
                save_patient_picture(current_user.id, image)

                flash('Profile picture uploaded successfully!', category='success')
            except Exception as e:
                error_msg = f"Could not upload profile picture: {e}"
                flash(error_msg, category='error')
        else:
            flash('Image format is invalid!', category='error')

    return redirect(url_for('views.patient_profile'))

@views.route('/upload-doctor-picture', methods=['POST'])
@login_required
def upload_doctor_picture():
    """" Uploads doctor's profile picture """
    if 'image' in request.files:
        image = request.files['image']
        
        if image and allowed_file(image.filename):
            try:
                save_doctor_picture(current_user.id, image)

                flash('Profile picture uploaded successfully!', category='success')
            except Exception as e:
                error_msg = f"Could not upload profile picture: {e}"
                flash(error_msg, category='error')
        else:
            flash('Image format is invalid!', category='error')

    return redirect(url_for('views.doctor_profile'))


@views.route('/update-doctor-profile', methods=['POST'])
@login_required
def update_doctor_profile():
    if request.method == 'POST':
        bio = request.form.get('bio')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Update doctor's bio and location in the database
        current_user.bio = bio
        current_user.latitude = latitude
        current_user.longitude = longitude
        db.session.commit()

        flash('Profile updated successfully!', category='success')

    return redirect(url_for('views.doctor_profile'))

@views.route('/specialists', methods=['GET'])
def our_specialists():
    search_query = request.args.get('search', '')
    
    if search_query:
        doctors = session.query(Doctor).filter(
            (Doctor.first_name.ilike(f"%{search_query}%")) |
            (Doctor.last_name.ilike(f"%{search_query}%"))
        ).all()
    else:
        doctors = session.query(Doctor).all()
    return render_template('specialists.html', doctors=doctors)

@views.route('/specializations/<int:specialization_id>/doctors', methods=['GET'])
def doctors_by_specialization(specialization_id):
    specialization = session.query(Specialization).get_or_404(specialization_id)
    doctors = session.query(Doctor).filter_by(speciality=specialization.name, approved=True).all()
    return render_template('doctors_by_specialization.html', specialization=specialization, doctors=doctors)

@views.route('/specializations', methods=['GET'])
def specializations():
    search_query = request.args.get('search', '')
    
    if search_query:
        specializations = session.query(Specialization).filter(Specialization.name.ilike(f"%{search_query}%")).all()
    else:
        specializations = session.query(Specialization).all()
    return render_template('specializations.html', specializations=specializations)

@views.route('/book_appointment/<int:doctor_id>', methods=['POST', 'GET'])
@login_required
def book_appointment(doctor_id):
    doctor = session.query(Doctor).filter(id=doctor_id).one()
    return render_template('book_appointment.html', calendly=doctor.calendly_link)

@views.route('/update-doctor-profile', methods=['POST'])
@login_required
def update_doctor_profile():
    if request.method == 'POST':
        bio = request.form.get('bio')
        calendly_link = request.form.get('calendly_link')
        location_iframe = request.form.get('location_iframe')

        # Update doctor's bio and location in the database
        current_user.bio = bio
        current_user.calendly_link = calendly_link
        current_user.location_iframe = location_iframe
        db.session.commit()

        flash('Profile updated successfully!', category='success')

    return redirect(url_for('views.doctor_profile'))

@views.route('/admin/pending_doctors')
# @login_required  # Ensure only admin can access
def view_pending_doctors():
    pending_doctors = Doctor.query.filter_by(approved=False).all()
    return render_template('pending_doctors.html', pending_doctors=pending_doctors)

@views.route('/admin/approve_doctor/<int:doctor_id>', methods=['POST'])
@login_required
@admin_required
def approve_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.approved = True

    # Replace these values with your Outlook account details
    email_address = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
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

    try:
        add_specialization(doctor.speciality)
    except Exception as e:
        print(e)

    # Commit changes to the database
    db.session.commit()

    flash('Doctor approved successfully.', 'success')
    return redirect(url_for('views.view_pending_doctors'))

@views.route('/admin/decline_doctor/<int:doctor_id>', methods=['POST'])
@login_required
@admin_required
def decline_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)

    # Replace these values with your Outlook account details
    email_address = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
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
    return redirect(url_for('views.view_pending_doctors'))


@views.route('/appointment/')

@views.route('/display/<int:id>')
def display(id):
    return render_template('display.html')
