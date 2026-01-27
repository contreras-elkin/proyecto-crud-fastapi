from sqlalchemy.orm import Session
from app.models.user_model import User

class UserRepository():

    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id):
        return self.db.get(User, user_id)

