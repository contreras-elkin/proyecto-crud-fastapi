from sqlalchemy.orm import Session
from app.exceptions.domain import UserEmailExists, UserNameExists, UserNotFoundError, UserPhoneExists
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserService:
    def __init__(self, db: Session, user_repository: UserRepository):
        self.db=db
        self.user_repository = user_repository
    
    def _hash_password(self, password: str) -> str:
        """Hash una contraseña"""
        return pwd_context.hash(password)
    
    def create(self, user_data: UserCreate) -> User:
        """Crear un nuevo usuario"""
        
        # Verificar si el email ya existe
        existing_email = self.user_repository.get_by_email(user_data.email)
        if existing_email:
            raise UserEmailExists(user_data.email)
        
        # Verificar si el username ya existe
        existing_username = self.user_repository.get_by_username(user_data.user_name)
        if existing_username:
            raise UserNameExists(user_data.user_name)
        
        # Crear nuevo usuario 
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["password"]= self._hash_password(user_data.password)
        user_new = User(**user_dict)

        self.user_repository.create(user_new)
        self.db.commit()
        self.db.refresh(user_new)
        
        return user_new
    
    def get_all(self, limit: int = 10, offset: int = 0) -> list[User]:
        """Obtener todos los usuarios"""
        return self.user_repository.get_all(limit, offset)
    
    def get_by_id(self, user_id: int) -> User | None:
        """Obtener usuario por ID"""
        user_db = self.user_repository.get_by_id(user_id)
        if not user_db:
            raise UserNotFoundError(user_id)
        
        return user_db
    
    def update(self, user_id: int, user_data: UserUpdate) -> User | None:
        """Actualizar un usuario"""
        
        # Validar que exista el usuario en BD
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        
        # Validar que el nuevo phone no exista en otro usuario
        if user_data.phone and user_data.phone != user.phone:
            existing = self.user_repository.get_by_phone(user_data.phone)
            if existing:
                raise UserPhoneExists(user_data.phone)
        
        # Validar que el nuevo email no exista en otro usuario
        if user_data.email and user_data.email != user.email:
            existing = self.user_repository.get_by_email(user_data.email)
            if existing:
                raise UserEmailExists(user_data.email)
        
        # Validar que el nuevo username no exista en otro usuario
        if user_data.user_name and user_data.user_name != user.user_name:
            existing = self.user_repository.get_by_username(user_data.user_name)
            if existing:
                raise UserNameExists(user_data.user_name)
        
        # Preparar datos para actualizar
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Hash password si se proporciona
        if "password" in update_data and update_data["password"]:
            update_data["password"] = self._hash_password(update_data["password"])
            
        self.user_repository.update(user, update_data)

        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete(self, user_id: int) -> bool:
        """Eliminar un usuario"""

        user_db = self.user_repository.get_by_id(user_id)
        if not user_db:
            raise UserNotFoundError(user_id)
        
        self.user_repository.delete(user_id)
        self.db.commit()
    
        
