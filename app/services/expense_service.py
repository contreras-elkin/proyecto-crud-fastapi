from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository



class ExpenseService:

    def __init__(self, repo: ExpenseRepository):
        self.repo=repo

    
    def create(self, expense: ExpenseCreate):

        new_expense = Expense(**expense.model_dump())
        return self.repo.create(new_expense)
    
    def get_all(self, limit, offset):

        return self.repo.get_all(limit, offset)
    
    def get_by_id(self, id_expense: int):
    
        return  self.repo.get_by_id(id_expense)
    
    def update(self, id_expense: int, expense: ExpenseUpdate):
        
        expense_update = expense.model_dump(exclude_unset=True)
        expense_data= self.repo.update(id_expense,expense_update)
        
        return expense_data

    def delete(self, id_expense:int):
        return self.repo.delete(id_expense)

       
        
