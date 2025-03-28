from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import and_, Numeric
from datetime import date
from decimal import Decimal
from app.security import verify_password, hash_password
from app.models import User


# Create a new expense record in the database
def create_expense(db: Session, expense_data: schemas.ExpenseApplicationCreate):
    new_expense = models.ExpenseApplication(**expense_data.dict())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# Retrieve all expenses from the database
def get_expenses(db: Session):
    return db.query(models.ExpenseApplication).all()


# Partially update an expense based on provided fields
def partial_update_expense(db: Session, expense_id: int, expense_data: schemas.ExpenseApplicationUpdate):
    expense = db.query(models.ExpenseApplication).filter(models.ExpenseApplication.id == expense_id).first()
    if expense is None:
        return None

    for key, value in expense_data.dict(exclude_unset=True).items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense


# Delete an expense by ID
def delete_expense(db: Session, expense_id: int):
    expense = db.query(models.ExpenseApplication).filter(models.ExpenseApplication.id == expense_id).first()
    if expense is None:
        return None
    db.delete(expense)
    db.commit()
    return f"The expense: {expense} was deleted successfully."


# Get a specific expense by its ID
def get_expense_by_id(db: Session, expense_id: int):
    return db.query(models.ExpenseApplication).filter(models.ExpenseApplication.id == expense_id).first()


# Apply multiple filters to search for expenses
def filter_expenses(db: Session,
                    expense_name: str = None,
                    expense_date: date = None,
                    deadline_payment: date = None,
                    status: str = None,
                    in_budget: bool = None,
                    start_date: date = None,
                    end_date: date = None,
                    start_amount: Decimal = None,
                    end_amount: Decimal = None,
                    start_deadline: date = None,
                    end_deadline: date = None,
                    sort_by: str = None,
                    sort_order: str = "asc",
                    ):
    query = db.query(models.ExpenseApplication)
    if expense_name:
        query = query.filter(models.ExpenseApplication.expense_name.ilike(f"%{expense_name}%"))
    if expense_date:
        query = query.filter(models.ExpenseApplication.expense_date == expense_date)
    if deadline_payment:
        query = query.filter(models.ExpenseApplication.deadline_payment == deadline_payment)
    if status:
        query = query.filter(models.ExpenseApplication.status.ilike(f"%{status}%"))
    if in_budget:
        query = query.filter(models.ExpenseApplication.in_budget == in_budget)
    if start_date and end_date:
        query = query.filter(and_(
            models.ExpenseApplication.expense_date >= start_date,
            models.ExpenseApplication.expense_date <= end_date,
        )
        )
    if start_amount and end_amount:
        query = query.filter(and_(
            models.ExpenseApplication.expense_amount >= start_amount,
            models.ExpenseApplication.expense_amount <= end_amount,
        )
        )
    if start_deadline and end_deadline:
        query = query.filter(and_(
            models.ExpenseApplication.deadline_payment >= start_deadline,
            models.ExpenseApplication.deadline_payment <= end_deadline,
        )
        )
    if sort_by:
        sort_field = getattr(models.ExpenseApplication, sort_by, None)
        if sort_field is not None:
            if sort_order == "desc":
                query = query.order_by(sort_field.desc())
            else:
                query = query.order_by(sort_field.asc())

    return query.all()


# Get a user from the database by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# Authenticate user by checking provided password against hashed password
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Create a new user with hashed password
def create_user(db: Session, user_data: schemas.UserCreate):
    hashed_pw = hash_password(user_data.password)
    new_user = models.User(
        username=user_data.username,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


