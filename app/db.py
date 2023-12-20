from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from .models import User, Doctor, Appointment, Review
from . import db
from werkzeug.security import generate_password_hash
import re
from typing import List

session = db.session

def find_user_by(email) -> User:
    """returns the first row found in the users table
    """
    if not email:
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
    
def find_doc(id) -> Doctor:
    """returns the first row found in the doctors table
    """
    if not id:
        raise ValueError
    try:
        return session.query(Doctor).filter_by(id=id).one()
    except NoResultFound:
        raise NoResultFound
    
def find_patient(id) -> User:
    """returns the first row found in the users table
    """
    if not id:
        raise ValueError
    try:
        return session.query(User).filter_by(id=id).one()
    except NoResultFound:
        raise NoResultFound