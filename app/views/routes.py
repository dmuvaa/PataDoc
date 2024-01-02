from flask import render_template, request, flash, redirect, url_for
from . import views
import os
from ..db import *
from flask_login import current_user, login_required


@views.route('/')
def index():
    return render_template('base.html')

@views.route('/profile/patient', methods=['GET'])
@login_required
def patient_profile():
    """ Renders the profile page once patient is logged in"""
    print(f'Session in patient profile: {session}')              
    user_type = session.get('user_type', 'user')
    print(f'Session in patient profile: {session}')              

    appointments = find_patient_app(current_user.id)
    reviews = []
    for appointment in appointments:
        review_info = {
            'review': find_rev(appointment.id),
            'doctor': find_doc(appointment.id)
        }
        reviews.append(review_info)
    return render_template('patient_profile.html', apps=appointments, current_user=current_user, revs=reviews, user_id=current_user.id,
                           user_type=user_type, image_exists=os.path.exists(f'static/user_profile/{current_user.id}.jpg'))

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
                           revs=reviews, user_id=current_user.id,
                           image_exists=os.path.exists(f'static/doctor_profile/{current_user.id}.jpg'))

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