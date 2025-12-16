
from sqlalchemy import Column, Integer, String, Float, Date
from datetime import date
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=True)
    time = Column(Date, default=date.today, nullable=False)
