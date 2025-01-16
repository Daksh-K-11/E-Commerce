from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {"message: Starting E-commerce"}

@app.get('/products')
def products():
    return {"message":'here will be post'}