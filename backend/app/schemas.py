from datetime import date, time, datetime
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str = "patient"

    class Config:
        from_attributes = True


class ScheduleBase(BaseModel):
    weekday: int
    start_time: time
    end_time: time


class ScheduleCreate(ScheduleBase):
    doctor_id: int


class ScheduleOut(ScheduleBase):
    id: int

    model_config = {"from_attributes": True}


class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    scheduled_time: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: int
    status: str

    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str


class UserCreate(UserBase):
    password: str


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
    user: UserOut

    model_config = {"from_attributes": True}


class PatientBase(BaseModel):
    medical_card_number: str
    date_of_birth: date


class PatientCreate(PatientBase):
    pass


class PatientOut(PatientBase):
    id: int
    user: UserOut

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
