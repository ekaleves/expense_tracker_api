from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
from fastapi import HTTPException
from typing import Optional, List, Literal
from datetime import date
from decimal import Decimal
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from app.auth import create_access_token
from app.crud import authenticate_user
from datetime import timedelta
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User


router = APIRouter()


# Create a new expense
@router.post("/expenses/", response_model=schemas.ExpenseApplication)
def created_expense(expense: schemas.ExpenseApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db=db, expense_data=expense)


# Get all expenses (requires valid user token)
@router.get("/expenses/", response_model=List[schemas.ExpenseApplication])
def read_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 👈 Requires a valid token
):
    return crud.get_expenses(db=db)


# Update an expense partially by ID
@router.patch("/expenses/", response_model=schemas.ExpenseApplication)
def patch_expense(expense_id: int, expense: schemas.ExpenseApplicationUpdate, db: Session = Depends(get_db)):
    updated = crud.partial_update_expense(db, expense_id, expense)
    if updated is None:
        raise HTTPException(status_code=404, detail="Expense not found.")
    return updated


# Search expenses with filters and optional sorting
@router.get("/expenses/search", response_model=List[schemas.ExpenseApplication])
def search_expenses(
        expense_name: Optional[str] = None,
        expense_date: Optional[date] = None,
        deadline_payment: Optional[date] = None,
        status: Optional[str] = None,
        in_budget: Optional[bool] = None,
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None),
        start_amount: Optional[Decimal] = Query(None),
        end_amount: Optional[Decimal] = Query(None),
        start_deadline: Optional[date] = Query(None),
        end_deadline: Optional[date] = Query(None),
        sort_by: Optional[str] = Query(
            None,
        description="Field to sort by. Options: id, expense_name, "
                    "expense_date, deadline_payment, status, "
                    "in_budget, expense_amount"),
        sort_order: Optional[str] = Query(
            "asc",
            description="Sort direction: 'asc' for ascending or "
                        "'desc' for descending"),
        db: Session = Depends(get_db),
):
    return crud.filter_expenses(db, expense_name, expense_date,
                                deadline_payment, status, in_budget,
                                start_date, end_date, start_amount,
                                end_amount, start_deadline, end_deadline,
                                sort_by, sort_order)


# Get a single expense by ID
@router.get("/expenses/{expense_id}", response_model=schemas.ExpenseApplication)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense_by_id(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found.")
    return expense


# Login route that returns an access token using OAuth2
@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": user.username},  # "sub" stands for subject (standard JWT claim)
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Register a new user
@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken."
        )
    return crud.create_user(db, user)

