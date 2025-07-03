from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Time,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, time


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    weekday = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    doctor = relationship("Doctor", backref="schedule")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")

    doctor = relationship("Doctor", backref="appointments")
    patient = relationship("Patient", backref="appointments")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    specialty = Column(String, nullable=False)
    room_number = Column(String, nullable=False)

    user = relationship("User", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    medical_card_number = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)

    user = relationship("User", back_populates="patient")
