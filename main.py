import schemas
import models
from models import User
from database import engine, SessionLocal, Base
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from utils import get_hashed_password

Base.metadata.create_all(bind=engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

@app.post("/register")
def register(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    encrypted_password = get_hashed_password(user.password)
    new_user = User(full_name=user.full_name, username=user.username, email=user.email, hashed_password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully"}
