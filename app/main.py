from fastapi import FastAPI
from  . import models
from .database import engine
from .routers import auth, register, product, cart, order, payment, rating, return_

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(register.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(payment.router)
app.include_router(rating.router)
app.include_router(return_.router)


@app.get('/')
def root():
    return {"message" : "Hey there it's me"}