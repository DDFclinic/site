from datetime import date, time, datetime
from typing import Literal
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "patient"


class UserPublic(BaseModel):
    full_name: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    date_of_birth: date


class UserOut(UserBase):
    id: int

    model_config = {"from_attributes": True}


class DoctorBase(BaseModel):
    specialty: str
    room_number: str


class DoctorCreate(DoctorBase):
    pass


class DoctorOut(DoctorBase):
    id: int
    user_id: int
    user: UserPublic

    model_config = {"from_attributes": True}


class PatientBase(BaseModel):
    medical_card_number: str


class PatientCreate(PatientBase):
    pass


class PatientOut(PatientBase):
    id: int
    user: UserOut

    model_config = {"from_attributes": True}


class ScheduleBase(BaseModel):
    weekday: int
    start_time: time
    end_time: time


class ScheduleCreate(ScheduleBase):
    doctor_id: int


class ScheduleOut(ScheduleBase):
    id: int
    doctor_id: int

    model_config = {"from_attributes": True}


class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    scheduled_time: datetime


class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_time: datetime


class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    status: Literal["scheduled", "completed", "cancelled"]

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    class Config:
        orm_mode = True


class DoctorRead(BaseModel):
    id: int
    user_id: int
    specialty: str
    room_number: str
    user: UserPublic

    model_config = {"from_attributes": True}

    class Config:
        orm_mode = True
