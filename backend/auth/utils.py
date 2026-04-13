from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:

    """
    Takes a plain text password and returns a bcrypt hash.
    This is used when a user registers — we never store
    the real password, only this hash.

    """

    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:

    """
    Checks if a plain text password matches a stored hash.
    This is used when a user logs in — we hash what they typed
    and compare it to what's stored in the database.
    Returns True if they match, False if they don't.

    """

    return pwd_context.verify(plain_password[:72], hashed_password)

