from fastapi import FastAPI
from app.models import expense, user_model
from app.routers import expenses
from app.core.database import Base, engine



app = FastAPI()

app.include_router(expenses.router)
 
Base.metadata.create_all(engine)

