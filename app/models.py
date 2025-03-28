from sqlalchemy import (Column, Integer, String, Date,
                        Boolean, Text, Numeric, UniqueConstraint)

from app.database import Base


# ExpenseApplication table to store expense records
class ExpenseApplication(Base):
    __tablename__ = "expenses"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    expense_name = Column(String, nullable=False)
    expense_date = Column(Date, nullable=True)
    deadline_payment = Column(Date, nullable=True)
    status = Column(String, default="open")
    description = Column(Text, nullable=True)
    in_budget = Column(Boolean, default=True)
    expense_amount = Column(Numeric, nullable=False)


# User table to store registered users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # 'unique' makes the data base have only unique users, like emails for eg
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)




