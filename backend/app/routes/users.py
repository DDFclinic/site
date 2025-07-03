from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    pwd_context,
    Token,
)
from app.database import get_db
from app import models
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.models import User
from app.auth import get_password_hash

router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "patient"
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    model_config = {"from_attributes": True}


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: models.User = Depends(get_current_active_user)):
    return current_user


from fastapi.security import OAuth2PasswordRequestForm


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    from datetime import timedelta
    from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    user.role = "patient"

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        role="patient",
        password_hash=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
