from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal


# Base schema for expenses (shared fields)
class ExpenseApplicationBase(BaseModel):
    expense_name: str
    expense_date: Optional[date] = None
    deadline_payment: Optional[date] = None
    status: Optional[str] = "open"
    description: Optional[str] = None
    in_budget: bool = True
    expense_amount: Optional[Decimal] = None


class ExpenseApplicationCreate(ExpenseApplicationBase):
    pass


class ExpenseApplication(ExpenseApplicationBase):
    id: int

    model_config = {
        "from_attributes": True  # Enables ORM compatibility
    }


# Schema for updating an expense (all fields optional)
class ExpenseApplicationUpdate(BaseModel):
    expense_name: Optional[str] = None
    expense_date: Optional[date] = None
    deadline_payment: Optional[date] = None
    status: Optional[str] = None
    description: Optional[str] = None
    in_budget: Optional[bool] = None
    expense_amount: Optional[Decimal] = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }
