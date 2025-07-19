from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Doctor
from app.schemas import DoctorRead

router = APIRouter(tags=["Doctors"])


@router.get("/", response_model=list[DoctorRead])
async def get_doctors(db: AsyncSession = Depends(get_db)):
    stmt = select(Doctor).options(selectinload(Doctor.user))
    result = await db.execute(stmt)
    doctors = result.scalars().all()
    return [DoctorRead.from_orm(doc) for doc in doctors]
