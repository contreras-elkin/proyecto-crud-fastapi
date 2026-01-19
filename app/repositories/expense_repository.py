from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.expense import Expense

class ExpenseRepository:
    def __init__(self, db: Session):
        self.db=db

    def create(self, expense: Expense):
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)

        return expense
    
    def get_all(self, limit, offset):
        
        return self.db.scalars(select(Expense).limit(limit).offset(offset)).all()
    
    def get_by_id(self, id_expense):
        return self.db.get(Expense, id_expense)
    
    def update(self, id_expense, expense_update):

        expense_db=self.db.get(Expense, id_expense)
        if not expense_db:
            return None
    
        for key, value in expense_update.items():
            setattr(expense_db, key, value)
        
        self.db.commit()
        self.db.refresh(expense_db)

        return expense_db
    
    def delete(self, id_expense):
        expense_db = self.db.get(Expense,id_expense)
        if not expense_db:
            return False
        
        self.db.delete(expense_db)
        self.db.commit()
        

        return True



        


