from datetime import datetime, timedelta
import bcrypt
import jwt
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth_app.models.database import Base, SessionLocal, engine
from auth_app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

SECRET_KEY = "super_secret_key"  # trzymane w zmiennych środowiskowych
ALGORITHM = "HS256"

DEFAULT_USERS = [
    {
        "username": "admin",
        "password": "admin123",
        "email": None,
    }
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def seed_default_users():
    with SessionLocal() as db:
        for default_user in DEFAULT_USERS:
            if db.query(User).filter(User.username == default_user["username"]).first():
                continue

            hashed_password = bcrypt.hashpw(
                default_user["password"].encode("utf-8"),
                bcrypt.gensalt(),
            ).decode("utf-8")

            user = User(
                username=default_user["username"],
                password_hash=hashed_password,
                email=default_user.get("email"),
                is_active=True,
            )
            db.add(user)
        db.commit()


class LoginData(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    username = data.username
    password = data.password.encode("utf-8")

    user = db.query(User).filter(User.username == username).first()

    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(password, user.password_hash.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
    "sub": username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    if data.email and db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = bcrypt.hashpw(
        data.password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

    user = User(
        username=data.username,
        password_hash=hashed_password,
        email=data.email,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user