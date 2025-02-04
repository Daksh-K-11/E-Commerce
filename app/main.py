from fastapi import FastAPI
from  . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import auth, register

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(register.router)


@app.get('/')
def root():
    return {"message" : "Hey there it's me"}