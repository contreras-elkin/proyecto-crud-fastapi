from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.exceptions.domain import ExpenseNotFoundError, UserNotFoundError



class ExpenseService:

    def __init__(self, db: Session,expense_repo: ExpenseRepository, user_repo: UserRepository):
        self.db=db
        self.expense_repo=expense_repo
        self.user_repo=user_repo

    
    def create(self, expense: ExpenseCreate):
        
        if not self.user_repo.get_by_id(expense.user_id):
            raise UserNotFoundError(expense.user_id)
       
        new_expense = Expense(**expense.model_dump())

        self.expense_repo.create(new_expense)

        self.db.commit()
        self.db.refresh(new_expense)

                
        return new_expense
        
    
    
    def get_all(self, limit, offset):

        return self.expense_repo.get_all(limit, offset)
    
    def get_by_id(self, expense_id: int):
        expense_db=self.expense_repo.get_by_id(expense_id)
        if not expense_db:
            raise ExpenseNotFoundError(expense_id)
        return  expense_db
    
    def update(self, expense_id: int, expense: ExpenseUpdate):

        # Validar que el gasto exista en BD
        expense_db=self.expense_repo.get_by_id(expense_id)
        if not expense_db:
            raise ExpenseNotFoundError(expense_id)
    
        data = expense.model_dump(exclude_unset=True)
        self.expense_repo.update(expense_db,data)

        self.db.commit()
        self.db.refresh(expense_db)
        
        return expense_db
    
    def delete(self, expense_id:int):
        # Validar que la entidad exista en BD
        expense_db = self.expense_repo.get_by_id(expense_id)
        if not expense_db:
            raise ExpenseNotFoundError(expense_id)
        
        self.expense_repo.delete(expense_db)
        self.db.commit()

        

       
        
