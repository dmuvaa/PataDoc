from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from .models import Specialization, User, Doctor, Admin, Appointment, Review
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
    if not is_valid_email(email):
        raise ValueError
    try:
        return session.query(Doctor).filter_by(email=email).one()
    except NoResultFound:
        raise NoResultFound


def add_doc(
        first_name, last_name, email, contact, password, speciality,
        bio, license_no, calendly_link, location_iframe):
    """ Add the doctor to the database"""
    doc = Doctor(
        first_name=first_name,
        last_name=last_name,
        email=email,
        contact=contact,
        password_hash=generate_password_hash(password),  # You need to hash the password
        speciality=speciality,
        bio=bio,
        license_no=license_no,
        calendly_link=calendly_link,
        location_iframe=location_iframe
    )

    try:
        session.add(doc)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
def register_doc(
        first_name, last_name, email, contact, password, speciality,
        bio, license_no, calendly_link, location_iframe):
        """ Check if doctor exists, if not, register the doctor
        """
        if is_valid_email(email.strip()):
            try:
                find_doc_by(email=email)
                raise ValueError("Doctor {} already exists".format(email))
            except NoResultFound:
                add_doc(
                    first_name, last_name, email, contact, password,
                    speciality, bio, license_no, calendly_link, location_iframe)
        else:
            raise ValueError("{} is invalid".format(email))

def find_patient_app(id) -> List[Appointment]:
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
        return session.query(Review).filter_by(appointment_id=appointment_id).one()
    except NoResultFound:
        raise NoResultFound

def find_doctor_app(id) -> List[Appointment]:
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
        print("No results found")
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

def save_review(appointment_id, rating, comment, doctor_id):
    review = Review(
        appointment_id=appointment_id,
        rating=rating,
        comment=comment,
        date_posted=datetime.utcnow(),
        doctor_id=doctor_id
        )
    try:
        db.session.add(review)
        db.session.commit()
    except Exception as e:
        session.rollback()
        raise e

def save_patient_picture(user_id, image) -> None:
    patient = find_patient(user_id) if find_patient(user_id) else None


    if patient is not None:
        save_directory = os.path.join('app/static', 'user_profile')
    else:
        raise ValueError("Invalid user type for patient")

    try:
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


def save_doctor_picture(user_id, image) -> None:

    doctor = find_doc(user_id) if find_doc(user_id) else None


    if doctor is not None:
        save_directory = os.path.join('app/static', 'doctor_profile')
    else:
        raise ValueError("Invalid user type for doctor")

    try:
        os.makedirs(save_directory, exist_ok=True)
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

def find_admin_by(email) -> Admin:
    """returns the first row found in the users table
    """
    if not is_valid_email(email):
        raise ValueError
    try:
        return session.query(Admin).filter_by(email=email).one()
    except NoResultFound:
        raise NoResultFound


def add_admin(first_name, last_name, email, contact_number, password):
    """ create an admin """
    admin = Admin(
        first_name=first_name,
        last_name=last_name,
        email=email,
        contact_number=contact_number,
        password_hash=generate_password_hash(password),  # You need to hash the password
        date_created=datetime.utcnow(),
    )

    try:
        session.add(admin)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def register_admin(first_name, last_name, email, contact_number, password):
        """ Check if admin exists, if not, register the admin
        """
        if is_valid_email(email.strip()):
            try:
                find_admin_by(email=email)
                raise ValueError("Admin {} already exists".format(email))
            except NoResultFound:
                add_admin(first_name, last_name, email, contact_number, password)
        else:
            raise ValueError("{} is invalid".format(email))
        
def find_specialization_by(name):
    """ Check if specialization is added"""
    try:
        return session.query(Specialization).filter_by(name=name).one()
    except NoResultFound:
        raise NoResultFound

        
def add_specialization(name):
    """ populate specialization table"""    
    try:
        find_specialization_by(name=name)
        pass
    except NoResultFound:
        specialization = Specialization(
        name=name,
        )
        try:
            session.add(specialization)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    