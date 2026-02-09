from fastapi import FastAPI
from app.models import expense, user_model
from app.routers import expenses, users
from app.core.database import Base, engine
from app.core.handlers import register_exceptions_handlers



app = FastAPI()

register_exceptions_handlers(app)
app.include_router(expenses.router)
app.include_router(users.router)
 
Base.metadata.create_all(engine)

