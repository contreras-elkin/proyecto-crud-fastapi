from pydantic import BaseModel, Field
from datetime import date 

class ExpenseCreate(BaseModel):
    description: str | None= None
    amount: float = Field(gt=0, description="El monto debe ser mayor a 0")
    category: str | None= None
    time: date | None=None
    
class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    time: date

    class Config:
        from_attributes = True

class ExpenseUpdate(BaseModel):
    description: str | None=None
    amount: float | None=Field(None, gt=0, description="El monto debe ser mayor a 0")
    category: str | None=None
    time: date | None=None
    