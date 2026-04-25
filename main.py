from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello Fast API"}


products = [
    Product(id = 1, name = "Phone", description = "A SmartPhone", price = 999.99, quantity = 50)
]

@app.get("/products")
def get_all_products():
    return products