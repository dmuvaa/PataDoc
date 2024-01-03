from flask import render_template, request, flash, redirect, url_for, session
from . import views
import os
from ..db import *
from flask_login import current_user, login_required

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    """ Checks whether the image file type is among the allowed extentions """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    """ Renders the profile page once doctor is logged in"""
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
    doctors = session.query(Doctor).all()
    return render_template('specialists.html', doctors=doctors)

@views.route('/book_appointment/<int:doctor_id>', methods=['POST', 'GET'])
@login_required
def book_appointment(doctor_id):
    
    return render_template('book_appointment.html')
