from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import TokenPayload

def create_access_token(data: dict) -> str:

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> TokenPayload:
    """
    Decodes a JWT token and returns the payload.
    Raises JWTError if the token is invalid or expired.

    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return TokenPayload(**payload)