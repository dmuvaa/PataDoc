from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from .models import User, Doctor, Appointment, Review
from . import db
import os
from werkzeug.security import generate_password_hash
import re
from typing import List, Optional

session = db.session

def find_user_by(email) -> User:
    """returns the first row found in the users table
    """
    if not is_valid_email(email):
        raise ValueError
    try:
        return session.query(User).filter_by(email=email).one()
    except NoResultFound:
        raise NoResultFound


def add_user(first_name, last_name, email, contact_number, password):
    """ create the user """
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        contact_number=contact_number,
        password_hash=generate_password_hash(password),  # You need to hash the password
        date_created=datetime.utcnow(),
    )

    try:
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    match = re.match(pattern, email)
    
    return bool(match)

def register_user(first_name, last_name, email, contact_number, password):
    """ Check if user exists, if not, register the user
    """
    if is_valid_email(email.strip()):
        try:
            find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            add_user(first_name, last_name, email, contact_number, password)
    else:
        raise ValueError("{} is invalid".format(email))

def find_doc_by(email) -> Doctor:
    """returns the first row found in the doctors table
    """
    if not email:
        raise ValueError
    try:
        return session.query(Doctor).filter_by(email=email).one()
    except NoResultFound:
        raise NoResultFound


def add_doc(
        first_name, last_name, email, contact, password, speciality,
        bio, license_no):
    """ Add the doctor to the database"""
    doc = Doctor(
        first_name=first_name,
        last_name=last_name,
        email=email,
        contact=contact,
        password_hash=generate_password_hash(password),  # You need to hash the password
        speciality=speciality,
        bio=bio,
        license_no=license_no
    )

    try:
        session.add(doc)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
def register_doc(
        first_name, last_name, email, contact, password, speciality,
        bio, license_no):
        """ Check if doctor exists, if not, register the doctor
        """
        if is_valid_email(email.strip()):
            try:
                find_doc_by(email=email)
                raise ValueError("Doctor {} already exists".format(email))
            except NoResultFound:
                add_doc(
                    first_name, last_name, email, contact, password,
                    speciality, bio, license_no)
        else:
            raise ValueError("{} is invalid".format(email))

def find_patient_app(id) -> List[User]:
    """returns the rows found in the appointments table
    """
    if not id:
        raise ValueError
    try:
        return session.query(Appointment).filter_by(patient_id=id).all()
    except NoResultFound:
        raise NoResultFound
    
def find_rev(appointment_id):
    """gets review of an appointment"""
    if not appointment_id:
        raise ValueError
    try:
        return session.query(Review).filter_by(appointment_id).one()
    except NoResultFound:
        raise NoResultFound

def find_doctor_app(id) -> List[Doctor]:
    """returns the rows found in the appointments table
    """
    if not id:
        raise ValueError
    try:
        return session.query(Appointment).filter_by(doctor_id=id).all()
    except NoResultFound:
        raise NoResultFound
    
def find_doc(id) -> Optional[Doctor]:
    """returns the first row found in the doctors table
    """
    if not id:
        raise ValueError
    try:
        return session.query(Doctor).filter_by(id=id).one()
    except NoResultFound:
        raise NoResultFound
    
def find_patient(id) -> Optional[User]:
    """returns the first row found in the users table
    """
    if not id:
        raise ValueError
    try:
        return session.query(User).filter_by(id=id).one()
    except NoResultFound:
        raise NoResultFound
    
def valid_review(doctor_id, appointment_id) -> Appointment:
    doctor = Doctor.query.get(doctor_id)
    appointment = Appointment.query.get(appointment_id)
    
    if doctor and appointment:
        return appointment
    else:
        return None

def save_review(appointment, rating, comment) -> bool:
    try:
        review = Review(appointment=appointment, rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()
    except Exception as e:
        session.rollback()
        raise e

def save_patient_profile(user_id, image) -> None:
    patient = find_patient(user_id) if find_patient(user_id) else None
    print(f'Is a patient: {patient}')

    if patient is not None:
        save_directory = os.path.join('app/static', 'user_profile')
    else:
        raise ValueError("Invalid user type for patient")

    try:
        print("Trying to save image")
        os.makedirs(save_directory, exist_ok=True)
        file_extension = os.path.splitext(image.filename)[1]  # Get the file extension
        save_path = os.path.join(save_directory, f'{user_id}.jpg')
        image.save(save_path)
        print("Image saved successfully")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise ValueError("Invalid file path")
    except IsADirectoryError as e:
        print(f"Error: {e}")
        raise ValueError("The specified path is a directory, not a file")
    except Exception as e:
        print(f"Error: {e}")
        raise ValueError("Failed to save the image")


def save_doctor_profile(user_id, image) -> None:
    doctor = find_doc(user_id) if find_doc(user_id) else None

    if doctor is not None:
        save_directory = os.path.join('app/static', 'doctor_profile')
    else:
        raise ValueError("Invalid user type for doctor")

    try:
        print("Trying to save image")
        os.makedirs(save_directory, exist_ok=True)
        file_extension = os.path.splitext(image.filename)[1]  # Get the file extension
        save_path = os.path.join(save_directory, f'{user_id}{file_extension}')
        image.save(save_path)
        print("Image saved successfully")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise ValueError("Invalid file path")
    except IsADirectoryError as e:
        print(f"Error: {e}")
        raise ValueError("The specified path is a directory, not a file")
    except Exception as e:
        print(f"Error: {e}")
        raise ValueError("Failed to save the image")


