from sqlalchemy import Numeric
from sqlalchemy import Column, Integer, String, Float, Date
from datetime import date
from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=True)
    amount = Column(Numeric(10,2), nullable=False)
    category = Column(String(50), nullable=True)
    expense_date = Column(Date, default=date.today, nullable=False)
