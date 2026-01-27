from app.repositories.user_repository import UserRepository
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.exceptions.domain import UserNotFoundError
from sqlalchemy.exc import IntegrityError


class ExpenseService:

    def __init__(self, expense_repo: ExpenseRepository, user_repo: UserRepository):
        self.expense_repo=expense_repo
        self.user_repo=user_repo

    
    def create(self, expense: ExpenseCreate):
        
        if not self.user_repo.get_by_id(expense.user_id):
            raise UserNotFoundError()
       
        new_expense = Expense(**expense.model_dump())
                
        return self.expense_repo.create(new_expense)
        
    
    
    def get_all(self, limit, offset):

        return self.expense_repo.get_all(limit, offset)
    
    def get_by_id(self, id_expense: int):
    
        return  self.expense_repo.get_by_id(id_expense)
    
    def update(self, id_expense: int, expense: ExpenseUpdate):
        
        expense_update = expense.model_dump(exclude_unset=True)
        expense_data= self.expense_repo.update(id_expense,expense_update)
        
        return expense_data

    def delete(self, id_expense:int):
        return self.expense_repo.delete(id_expense)

       
        
