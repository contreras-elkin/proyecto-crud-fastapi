from app.exceptions.domain import ExpenseNotFoundError, UserNotFoundError
from fastapi import APIRouter, Depends, HTTPException, Query,status, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expense_service import ExpenseService
from app.repositories.expense_repository import ExpenseRepository

router = APIRouter(prefix="/expenses", tags=["expenses"])



# Inject service
def get_expense_service(db: Session=Depends(get_db)) -> ExpenseService:
    expense_repository= ExpenseRepository(db)
    user_repository= UserRepository(db)
    return ExpenseService(db,expense_repository, user_repository)

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

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense_by_id(expense_id: int, expense_service: ExpenseService=Depends(get_expense_service)):
    
    return expense_service.get_by_id(expense_id)

@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate, expense_service: ExpenseService=Depends(get_expense_service)):
    
    return expense_service.update(expense_id, expense)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, expense_service: ExpenseService=Depends(get_expense_service)):

    expense_service.delete(expense_id)
    
        
    



    
