from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.PatientOut)
def create_patient(
    patient: schemas.PatientCreate, user_id: int, db: Session = Depends(get_db)
):
    user = db.query(models.User).get(user_id)
    if not user or user.role != "patient":
        raise HTTPException(status_code=400, detail="Invalid patient user")

    new_patient = models.Patient(user_id=user_id, **patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient
