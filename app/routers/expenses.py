from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate


router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model = ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session= Depends(get_db)):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/", response_model=list[ExpenseResponse])
def get_all_expenses(
    db: Session=Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return db.scalars(select(Expense).limit(limit).offset(offset)).all()

@router.get("/{id_expense}")
def get_expense_by_id(id_expense: int, db:Session= Depends(get_db)):
    expense=db.get(Expense, id_expense)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail=f"Gasto para el id {id_expense} no encontrado"
        )
    
    return expense

@router.patch("/{id_expense}", response_model=ExpenseResponse)
def update_expense(id_expense: int, expense: ExpenseUpdate, db: Session=Depends(get_db)):

    expense_data=db.get(Expense,id_expense)
    if expense_data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Gasto para el id {id_expense} no encontrado"
        )

    expense_update = expense.model_dump(exclude_unset=True)

    for key, value in expense_update.items():
        setattr(expense_data, key, value)

    db.commit()
    db.refresh(expense_data)

    return expense_data
    
