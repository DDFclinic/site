from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import models, schemas
from ..database import SessionLocal
from app.dependencies import get_current_user
from sqlalchemy.future import select

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.PatientOut)
async def create_patient(
    patient: schemas.PatientCreate, user_id: int, db: AsyncSession = Depends(get_db)
):
    user = await db.query(models.User).get(user_id)
    if not user or user.role != "patient":
        raise HTTPException(status_code=400, detail="Invalid patient user")

    new_patient = models.Patient(user_id=user_id, **patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.get("/medical_card", response_model=str)
async def get_medical_card_number(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(models.Patient).where(models.Patient.user_id == current_user.id)
    )
    patient = result.scalars().first()
    if not patient:
        raise HTTPException(status_code=404, detail="Пациент не найден")
    return patient.medical_card_number
