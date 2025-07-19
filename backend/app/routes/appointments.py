from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.dependencies import get_current_user
from app import models, schemas
from datetime import datetime

router = APIRouter(tags=["appointments"])


@router.get("/occupied")
async def get_occupied_slots(
    doctor_id: int = Query(...),
    date: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    start_datetime = datetime.fromisoformat(f"{date}T00:00:00")
    end_datetime = datetime.fromisoformat(f"{date}T23:59:59")

    stmt = select(models.Appointment.appointment_time).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_time >= start_datetime,
        models.Appointment.appointment_time <= end_datetime,
    )
    result = await db.execute(stmt)
    times = result.scalars().all()

    occupied_times = [t.strftime("%H:%M") for t in times]

    return occupied_times


@router.post("/")
async def create_appointment(
    data: schemas.AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not current_user.patient:
        raise HTTPException(status_code=403, detail="Вы не пациент")

    if data.appointment_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Нельзя записаться в прошлое")

    result = await db.execute(
        select(models.Appointment).filter(
            models.Appointment.doctor_id == data.doctor_id,
            models.Appointment.appointment_time == data.appointment_time,
        )
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=409, detail="Это время уже занято")

    new_appointment = models.Appointment(
        patient_id=current_user.patient.id,
        doctor_id=data.doctor_id,
        appointment_time=data.appointment_time,
    )
    db.add(new_appointment)
    await db.commit()
    await db.refresh(new_appointment)

    return {"message": "Запись успешна", "appointment_id": new_appointment.id}


@router.get("/my")
async def get_my_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    stmt = (
        select(models.Appointment, models.Doctor, models.User)
        .join(models.Doctor, models.Appointment.doctor_id == models.Doctor.id)
        .join(models.User, models.Doctor.user_id == models.User.id)
        .filter(models.Appointment.patient_id == current_user.patient.id)
        .order_by(models.Appointment.appointment_time)
    )
    result = await db.execute(stmt)
    rows = result.all()

    appointments = []
    for appointment, doctor, user in rows:
        appointments.append(
            {
                "id": appointment.id,
                "appointment_time": appointment.appointment_time.isoformat(),
                "doctor": {
                    "id": doctor.id,
                    "specialty": doctor.specialty,
                    "full_name": user.full_name,
                },
            }
        )

    return appointments


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(
        select(models.Appointment).filter(models.Appointment.id == appointment_id)
    )
    appointment = result.scalars().first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    if appointment.patient_id != current_user.patient.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этой записи")

    await db.delete(appointment)
    await db.commit()

    return None
