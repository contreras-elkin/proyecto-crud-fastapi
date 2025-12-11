from fastapi import FastAPI
from app.routers import expenses

from app.database import Base, engine


app = FastAPI()

app.include_router(expenses.router)
 
Base.metadata.create_all(engine)

