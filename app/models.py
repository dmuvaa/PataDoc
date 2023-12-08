from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    user_data = relationship("UserData", back_populates="user", uselist=False)
    doctor = relationship("Doctor", back_populates="user", uselist=False)

class UserData(Base):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime)
    gender = Column(String)
    contact_number = Column(String)

    user = relationship("User", back_populates="user_data")

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bio = Column(String)
    profile_picture_url = Column(String)
    years_of_experience = Column(Integer)
    
    user = relationship("User", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    specializations = relationship("DoctorSpecialization", back_populates="doctor")

class Specialization(Base):
    __tablename__ = 'specializations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class DoctorSpecialization(Base):
    __tablename__ = 'doctor_specializations'

    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specializations.id'), primary_key=True)

    doctor = relationship("Doctor", back_populates="specializations")
    specialization = relationship("Specialization")

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    purpose = Column(String)
    notes = Column(String)

    patient = relationship("User")
    doctor = relationship("Doctor", back_populates="appointments")

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=False)
    rating = Column(Float)
    comment = Column(String)
    date_posted = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment")

# Add the database URL
engine = create_engine('postgresql://username:password@localhost/mydatabase')

# Create all tables in the database
Base.metadata.create_all(engine)
