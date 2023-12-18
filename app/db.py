from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from .models import User, Doctor
from . import db
from werkzeug.security import generate_password_hash
import re

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
        date_created=datetime.utcnow()
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
        if is_valid_email(email):
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


def add_doc(first_name, last_name, email, contact_number, password):
    """ Add the doctor to the database"""
    doc = Doctor(
        first_name=first_name,
        last_name=last_name,
        email=email,
        contact_number=contact_number,
        password_hash=generate_password_hash(password),  # You need to hash the password
        date_created=datetime.utcnow()
    )

    try:
        session.add(doc)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
def register_doc(first_name, last_name, email, contact_number, password):
        """ Check if doctor exists, if not, register the doctor
        """
        if is_valid_email(email):
            try:
                find_doc_by(email=email)
                raise ValueError("Doctor {} already exists".format(email))
            except NoResultFound:
                add_doc(first_name, last_name, email, contact_number, password)
        raise ValueError("{} is invalid".format(email))