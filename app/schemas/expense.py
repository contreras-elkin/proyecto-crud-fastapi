from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import date 

class ExpenseCreate(BaseModel):
    description: str | None= None
    amount: Decimal = Field(gt=0, description="El monto debe ser mayor a 0")
    category: str | None= None
    expense_date: date | None=None
    
class ExpenseResponse(BaseModel):
    id: int
    description: str | None
    amount: Decimal 
    category: str | None
    expense_date: date

    class Config:
        from_attributes = True

class ExpenseUpdate(BaseModel):
    description: str | None=None
    amount: Decimal | None=Field(None, gt=0, description="El monto debe ser mayor a 0")
    category: str | None=None
    expense_date: date | None=None
    