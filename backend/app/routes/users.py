from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, Patient
from app.schemas import UserCreate, UserResponse, Token
from app.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    pwd_context,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter()


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    model_config = {"from_attributes": True}


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        password_hash=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user.role = "patient"
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        date_of_birth=user.date_of_birth,
        role="patient",
        password_hash=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    medical_card_number = f"MC{db_user.id:04d}"
    new_patient = Patient(
        user_id=db_user.id,
        medical_card_number=medical_card_number,
        date_of_birth=user.date_of_birth,
    )
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)

    return db_user
