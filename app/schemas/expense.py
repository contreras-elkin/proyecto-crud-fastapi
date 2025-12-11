from pydantic import BaseModel, Field

class ExpenseCreate(BaseModel):
    description: str # = Field(..., min_length=1, description="La descripción es obligatoria")
    amount: float = Field(gt=0, description="El monto debe ser mayor a 0")
    category: str = Field(..., min_length=1, description="La categoría es obligatoria") 

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str

    class Config:
        from_attributes = True

class ExpenseUpdate(BaseModel):
    description: str | None=None#Field(None, min_length=1)
    amount: float | None=Field(None, gt=0, description="El monto debe ser mayor a 0")
    category: str | None=Field(None, min_length=1)
