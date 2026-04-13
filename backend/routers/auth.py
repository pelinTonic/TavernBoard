from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from model import User
from schemas import UserCreate, UserRead
from auth.utils import hash_password, verify_password
from auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.
    Checks if username is already taken, hashes the password,
    saves the user to the database.
    """
    # Check if username already exists
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Hash the password before saving
    new_user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
        role=data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": user.id, "role": user.role.value})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {                   # ← add this so frontend has user info
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }