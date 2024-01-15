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

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    contact_number = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        """ Format the Admin object"""
        return ("<Admin(id={}, email={}, password_hash={}, firstname={}, lastname={}, contact={})>"  # noqa: E501
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
    license_no = db.Column(db.String, unique=True, nullable=False)
    calendly_link = db.Column(db.String(1000))
    location_iframe = db.Column(db.String(1000))
    approved = db.Column(db.Boolean, default=False)
    
    appointments = db.relationship("Appointment", back_populates="doctor")
    reviews = db.relationship("Review", back_populates="doctor")

    def __repr__(self):
        """ Format the Doctor object"""
        return (
            "<Doctor(id={}, email={}, password_hash={}, firstname={}, "
            "lastname={}, contact={}, speciality={}, bio={}, "
            "license_no{}, approved={}, calendly_link={}, location_iframe={})>"
                .format(self.id, self.email, self.password_hash,
                        self.first_name, self.last_name, self.contact,
                        self.speciality, self.bio, self.license_no,
                        self.approved, self.calendly_link, self.location_iframe
                        ))

class Specialization(db.Model):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    

    def __repr__(self):
        """ Format the Specialization object"""
        return ("<Specialization(id={}, name={}>"
                .format(self.id, self.name))


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
    reviews = db.relationship("Review", back_populates="appointment")

    def __repr__(self):
        """ Format the Appointment object"""
        return (
            "<Appointment(id={}, patient_id={}, doctor_id={}, "
            "appointment_time={}, status={}, purpose={}, notes={})>"
                .format(self.id, self.patient_id, self.doctor_id,
                        self.appointment_time, self.status, self.purpose,
                        self.notes))

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    appointment = db.relationship("Appointment", back_populates="reviews")
    doctor = db.relationship("Doctor", back_populates="reviews")

    def __repr__(self):
        """ Format the Review object"""
        return (
            "<Review(id={}, appointment_id={}, rating={}, "
            "comment={}, date_posted={}, doctor_id)>"
                .format(self.id, self.appointment_id, self.rating,
                        self.comment, self.date_posted, self.doctor_id))