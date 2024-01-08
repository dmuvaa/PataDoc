from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    contact_number = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        """ Format the User object"""
        return ("<User(id={}, email={}, password_hash={}, firstname={}, lastname={}, contact={})>"  # noqa: E501
                .format(self.id, self.email, self.password_hash,
                        self.first_name, self.last_name, self.contact_number))


class Doctor(db.Model, UserMixin):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    contact = db.Column(db.String)
    password_hash = db.Column(db.String, nullable=False)
    speciality = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    profile_picture_url = db.Column(db.String)
    license_no = db.Column(db.String, unique=True, nullable=False)
    
    appointments = db.relationship("Appointment", back_populates="doctor")
    specializations = db.relationship("DoctorSpecialization", back_populates="doctor")

    def __repr__(self):
        """ Format the Doctor object"""
        return (
            "<Doctor(id={}, email={}, password_hash={}, firstname={}, "
            "lastname={}, contact={}, speciality={}, bio={}, "
            "profile_picture_url={}, license_no{})>"
                .format(self.id, self.email, self.password_hash,
                        self.first_name, self.last_name, self.contact,
                        self.speciality, self.bio, self.profile_picture_url,
                        self.license_no))

class Specialization(db.Model):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class DoctorSpecialization(db.Model):
    __tablename__ = 'doctor_specializations'

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), primary_key=True)

    doctor = db.relationship("Doctor", back_populates="specializations")
    specialization = db.relationship("Specialization")

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False)
    purpose = db.Column(db.String)
    notes = db.Column(db.String)

    patient = db.relationship("User")
    doctor = db.relationship("Doctor", back_populates="appointments")

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    rating = db.Column(db.Float)
    comment = db.Column(db.String)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    appointment = db.relationship("Appointment")
