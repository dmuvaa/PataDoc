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
import pickle
from datetime import timedelta
import redis
from app import redis_client

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
    reviews = {}
    for appointment in appointments:
        try:
            review = find_rev(appointment.id)
        except NoResultFound:
            review = None

        try:
            doctor = find_doc(appointment.doctor_id)
        except NoResultFound:
            doctor = None

        review_info = {
            'review': review,
            'doctor': doctor
        }
        app_id = appointment.id
        reviews[app_id] = review_info

    return render_template('patient_profile.html', apps=appointments, current_user=current_user, revs=reviews, user_id=str(current_user.id),
                        image_exists=os.path.exists(f'app/static/user_profile/{current_user.id}.jpg'))

@views.route('/profile/doctor', methods=['GET'])
@login_required
def doctor_profile():
    """ Renders the profile page once doctor is logged in """
    doctor_id = current_user.id
    cache_key = f"doctor_profile_{doctor_id}"

    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            appointments, reviews = pickle.loads(cached_data)
        else:
            appointments, reviews = fetch_doctor_data(doctor_id)
            redis_client.setex(cache_key, timedelta(hours=3), pickle.dumps((appointments, reviews)))

    except (redis.RedisError, pickle.PickleError, KeyError):
        appointments, reviews = fetch_doctor_data(doctor_id)

    return render_template('doctor_profile.html', current_user=current_user, apps=appointments,
                           revs=reviews, user_id=str(doctor_id),
                           image_exists=os.path.exists(os.path.join('app/static/doctor_profile', f'{doctor_id}.jpg')))

def fetch_doctor_data(doctor_id):
    appointments = find_doctor_app(doctor_id)
    reviews = {}
    for appointment in appointments:
        try:
            review = find_rev(appointment.id)
        except NoResultFound:
            review = None

        try:
            patient = find_patient(appointment.patient_id)
        except NoResultFound:
            patient = None

        review_info = {
            'review': review,
            'patient': patient
        }
        app_id = appointment.id
        reviews[app_id] = review_info

    return appointments, reviews

@views.route('/leave-review/<int:doctor_id>/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def leave_review(doctor_id, appointment_id):

    if not valid_review(doctor_id, appointment_id):
        flash('Invalid doctor or appointment.', 'error')
        return redirect(url_for('views.patient_profile'))
    
    appointment = valid_review(doctor_id, appointment_id)
    doctor = find_doc(doctor_id)

    if request.method == 'POST':
        rating = float(request.form.get('rating'))
        comment = request.form.get('comment')


        try:
            save_review(appointment_id, rating, comment, doctor_id)
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('views.patient_profile'))
        except Exception as e:
            flash('Could not submit review!', 'error')
            return redirect(url_for('views.index'))

    return render_template('leave_review.html', doctor=doctor, appointment=appointment)

@views.route('/upload-user-picture', methods=['POST'])
@login_required
def upload_user_picture():
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

@views.route('/specialists', methods=['GET'])
def our_specialists():
    search_query = request.args.get('search', '')
    specialization = request.args.get('specialization', '')
    cache_key = f"specialists_{search_query}_{specialization}"
    images = {}

    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            doctors = pickle.loads(cached_data)
        else:
            raise KeyError("Data not in cache")
    except (KeyError, redis.RedisError):
        if search_query:
            doctors = session.query(Doctor).filter(
                (Doctor.first_name.ilike(f"%{search_query}%")) |
                (Doctor.last_name.ilike(f"%{search_query}%"))
            ).all()
        elif specialization:
            doctors = session.query(Doctor).filter(Doctor.speciality == specialization).all()
        else:
            doctors = session.query(Doctor).all()
        for doctor in doctors:
            if os.path.exists(f'app/static/doctor_profile/{doctor.id}.jpg'):
                image_exists = True
            else:
                image_exists = False

            doc_id = doctor.id
            doc_dict = {
                'image': image_exists,
                'str_id': str(doc_id)
            }
            images[doc_id] = doc_dict
        redis_client.setex(cache_key, timedelta(hours=3), pickle.dumps(doctors))
    else:
        # If doctors are retrieved from the cache, check if the data needs to be updated
        if search_query:
            doctors = session.query(Doctor).filter(
                (Doctor.first_name.ilike(f"%{search_query}%")) |
                (Doctor.last_name.ilike(f"%{search_query}%"))
            ).all()
        elif specialization:
            doctors = session.query(Doctor).filter(Doctor.speciality == specialization).all()
        else:
            doctors = session.query(Doctor).all()
        for doctor in doctors:
            if os.path.exists(f'app/static/doctor_profile/{doctor.id}.jpg'):
                image_exists = True
            else:
                image_exists = False

            doc_id = doctor.id
            doc_dict = {
                'image': image_exists,
                'str_id': str(doc_id)
            }
            images[doc_id] = doc_dict
        redis_client.setex(cache_key, timedelta(hours=3), pickle.dumps(doctors))
    
    return render_template('specialists.html', doctors=doctors, images=images)


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
    print("Email Address:", email_address)

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


@views.route('/reviews/<int:id>', methods=['GET'])
def reviews(id):
    """Retrieves all reviews for the doctor"""
    appointments = find_doctor_app(id)
    reviews = {}
    doctor = find_doc(id)
    for appointment in appointments:
        try:
            review = find_rev(appointment.id)
        except NoResultFound:
            review = None

        try:
            patient = find_patient(appointment.patient_id)
        except NoResultFound:
            patient = None

        review_info = {
            'review': review,
            'patient': patient
        }
        app_id = appointment.id
        reviews[app_id] = review_info

    return render_template('reviews.html', apps=appointments, revs=reviews,
                           doctor=doctor, user_id=str(id),
                           image_exists=os.path.exists(f'app/static/doctor_profile/{id}.jpg'))
