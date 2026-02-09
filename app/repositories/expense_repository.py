from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.expense import Expense

class ExpenseRepository:
    def __init__(self, db: Session):
        self.db=db

    def create(self, expense: Expense):
        
        self.db.add(expense)
    
        return expense
     
    def get_all(self, limit, offset):
        
        return self.db.scalars(select(Expense).limit(limit).offset(offset)).all()
    
    def get_by_id(self, expense_id):
        return self.db.get(Expense, expense_id)
    
    def update(self, expense_db, data):

        for key, value in data.items():
            setattr(expense_db, key, value)
    
        return expense_db
    
    def delete(self, expense_db):
        self.db.delete(expense_db)
        



        


