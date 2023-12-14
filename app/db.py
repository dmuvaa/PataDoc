import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from .models import User
from . import db

session = db.session


def hash_password(password):
    """ hash the password """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

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
        password_hash=hash_password(password),  # You need to hash the password
        date_created=datetime.utcnow()
    )

    try:
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def register_user(first_name, last_name, email, contact_number, password):
        """ Check if user exists, if not, register the user
        """
        try:
            find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            add_user(first_name, last_name, email, contact_number, password)