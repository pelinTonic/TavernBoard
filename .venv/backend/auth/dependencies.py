from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from auth.jwt import decode_access_token
from database import get_db
from model import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Reads the JWT from the Authorization header,
    decodes it, and fetches the matching user from the DB.
    Raises 401 if token is invalid or user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.sub
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def require_dm(current_user: User = Depends(get_current_user)) -> User:
    """
    Calls get_current_user first, then checks if the user is a DM.
    Raises 403 if the user is not a DM.
    Use this dependency on any route that only DMs can access.
    """
    if current_user.role != "dm":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Dungeon Masters can do this"
        )
    return current_user