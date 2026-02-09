from sqlalchemy.orm import Session
from app.models.user_model import User

class UserRepository():

    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int):
        return self.db.get(User, user_id)
    
    def create(self, user: User) -> User:
        """Crear un nuevo usuario"""
        self.db.add(user)
        
        return user
    
    def get_all(self, limit: int = 10, offset: int = 0) -> list[User]:
        """Obtener todos los usuarios con paginación"""
        return self.db.query(User).limit(limit).offset(offset).all()
    
    def get_by_email(self, email: str) -> User | None:
        """Obtener usuario por email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> User | None:
        """Obtener usuario por nombre de usuario"""
        return self.db.query(User).filter(User.user_name == username).first()
    
    def get_by_phone(self, phone:str) -> User | None:
        return self.db.query(User).filter(User.phone == phone).first()

    
    def update(self, user: User, user_data: dict) -> User | None:
        """Actualizar un usuario"""
        
        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)
        
        return user
    
    def delete(self, user_id: int) -> None:
        """Eliminar un usuario"""
        self.db.delete(user_id)
        
        

