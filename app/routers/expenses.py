from fastapi import APIRouter, Depends, HTTPException, Query,status, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expense_service import ExpenseService
from app.repositories.expense_repository import ExpenseRepository

router = APIRouter(prefix="/expenses", tags=["expenses"])

# Inject repository
def get_expense_repository(db: Session=Depends(get_db)) -> ExpenseRepository:
        return ExpenseRepository(db)

# Inject service
def get_expense_service(expense_repository: ExpenseRepository=Depends(get_expense_repository)) -> ExpenseService:
    return ExpenseService(expense_repository)

@router.post("/", response_model = ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, response: Response, expense_service: ExpenseService=Depends(get_expense_service)):
    
    new_expense = expense_service.create(expense)
    response.headers["Location"] = f"/expenses/{new_expense.id}"

    return new_expense

@router.get("/", response_model=list[ExpenseResponse])
def get_all_expenses(
    expense_service: ExpenseService =Depends(get_expense_service),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return expense_service.get_all(limit, offset)

@router.get("/{id_expense}", response_model=ExpenseResponse)
def get_expense_by_id(id_expense: int, expense_service: ExpenseService=Depends(get_expense_service)):
    
    expense= expense_service.get_by_id(id_expense)
    if expense is None:
        raise HTTPException(
            status_code=404,
            detail=f"Gasto para el id {id_expense} no encontrado"
        )
    return expense

@router.patch("/{id_expense}", response_model=ExpenseResponse)
def update_expense(id_expense: int, expense: ExpenseUpdate, expense_service: ExpenseService=Depends(get_expense_service)):

    expense_data=expense_service.update(id_expense, expense)
    if not expense_data:
        raise HTTPException(
            status_code=404,
            detail=f"Gasto para el id {id_expense} no encontrado"
        )

    return expense_data


@router.delete("/{id_expense}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id_expense: int, expense_service: ExpenseService=Depends(get_expense_service)):

    expense = expense_service.delete(id_expense)
    if not expense:
        raise HTTPException(
            status_code=404,
            detail=f"Gasto para el id {id_expense} no encontrado"
        )
    
    



    
