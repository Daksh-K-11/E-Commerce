from fastapi import FastAPI
from  . import models
from .database import engine
from .routers import auth, register, product, cart, order

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(register.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)



@app.get('/')
def root():
    return {"message" : "Hey there it's me"}