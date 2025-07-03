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


@router.post("/", response_model=schemas.DoctorOut)
def create_doctor(
    doctor: schemas.DoctorCreate, user_id: int, db: Session = Depends(get_db)
):
    user = db.query(models.User).get(user_id)
    if not user or user.role != "doctor":
        raise HTTPException(status_code=400, detail="Invalid doctor user")

    new_doc = models.Doctor(user_id=user_id, **doctor.dict())
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc
