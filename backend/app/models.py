from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Time,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
from .database import Base
import enum


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    weekday = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    doctor = relationship("Doctor", back_populates="schedules")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    status = Column(
        Enum(AppointmentStatus), default=AppointmentStatus.scheduled, nullable=False
    )

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)

    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    specialty = Column(String, nullable=False)
    room_number = Column(String, nullable=False)

    user = relationship("User", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    schedules = relationship("Schedule", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    medical_card_number = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)

    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
