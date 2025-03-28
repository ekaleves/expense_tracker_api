from passlib.context import CryptContext


# Initialize password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash a plain text password for secure storage
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verify a plain password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = pwd_context.verify(plain_password, hashed_password)
    return result
