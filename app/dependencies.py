from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import get_user_by_username
from app.models import User
from app.auth import SECRET_KEY, ALGORITHM
from app.database import get_db


# Define the OAuth2 scheme using HTTP Bearer tokens
oauth2_scheme = HTTPBearer()


# Dependency to extract and validate the current user from the token
def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    # Exception raised for invalid or missing credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, # status from the file status.py
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # Decode JWT token and extract the username (subject)
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Retrieve user from the database
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user
