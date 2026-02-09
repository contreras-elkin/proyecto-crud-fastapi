from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])



# Inyectar servicio 
def get_user_service(db: Session=Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(db,user_repository)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, response: Response, user_service: UserService = Depends(get_user_service)):

    new_user = user_service.create(user)
    response.headers["Location"] = f"/users/{new_user.id}"
    
    return new_user
    


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    user_service: UserService = Depends(get_user_service),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return user_service.get_all(limit, offset)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)):
    
    return user_service.get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
   
    return user_service.update(user_id, user_data)
    


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    
    user_service.delete(user_id)
    
