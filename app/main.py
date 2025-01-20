from fastapi import FastAPI, status, HTTPException, Depends
from  . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def root():
    return {"message: Starting E-commerce"}

@app.get('/products')
def products():
    return {"message":'here will be post'}

@app.get('/test')
def test(db : Session = Depends(get_db)):
    return {"test": "test"}