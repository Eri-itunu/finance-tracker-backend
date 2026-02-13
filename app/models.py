from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from .database import Base
import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum




class Currency(str, Enum):
    NGN = "NGN"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"

class User(Base): # User model DONE
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    categories = relationship("Category", back_populates="user")
    incomes = relationship("Income", back_populates="user")
    spendings = relationship("Spending", back_populates="user")
    savings_goals = relationship("SavingsGoal", back_populates="user")
    savings_contributions = relationship("SavingsContribution", back_populates="user")
    default_currency = Column(SQLEnum(Currency), default=Currency.NGN, nullable=False)

class Category(Base): # Category model DONE
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="categories")
    spendings = relationship("Spending", back_populates="category")

class Income(Base): # Income model DONE
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    source = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String) # "cash" or "card"
    currency = Column(SQLEnum(Currency), default=Currency.NGN, nullable=False)


    user = relationship("User", back_populates="incomes")

class Spending(Base): # Spending model DONE
    __tablename__ = "spending"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    notes = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    item_name = Column(String)
    is_deleted = Column(Boolean, default=False)
    user = relationship("User", back_populates="spendings")
    category = relationship("Category", back_populates="spendings")
    currency = Column(SQLEnum(Currency), default=Currency.NGN, nullable=False)

class SavingsGoal(Base): # SavingsGoal model DONE
    __tablename__ = "savings_goals"

    id = Column(Integer, primary_key=True, index=True)
    goal_name = Column(String)
    target_amount = Column(Float)
    deadline = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="savings_goals")
    savings_contributions = relationship("SavingsContribution", back_populates="savings_goal")
    currency = Column(SQLEnum(Currency), default=Currency.NGN, nullable=False)

class SavingsContribution(Base): # SavingsContribution model DONE
    __tablename__ = "savings_contributions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    goal_id = Column(Integer, ForeignKey("savings_goals.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    savings_goal = relationship("SavingsGoal", back_populates="savings_contributions")
    user = relationship("User", back_populates="savings_contributions")
    currency = Column(SQLEnum(Currency), default=Currency.NGN, nullable=False)


# class ExchangeRate(Base):
#     __tablename__ = "exchange_rates"
    
#     id = Column(Integer, primary_key=True, index=True)
#     from_currency = Column(SQLEnum(Currency), nullable=False)
#     to_currency = Column(SQLEnum(Currency), nullable=False)
#     rate = Column(Float, nullable=False)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
#     __table_args__ = (
#         UniqueConstraint('from_currency', 'to_currency', name='uix_currency_pair'),
#     )