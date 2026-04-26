from fastapi import FastAPI, Depends
from models import Product
from database import engine, session
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Hello Fast API"}


products = [
    Product(id = 1, name = "Phone", description = "A SmartPhone", price = 999.99, quantity = 50),
    Product(id = 2, name = "Laptop", description = "A Laptop", price = 8999.99, quantity = 30),
    Product(id = 3, name = "Bag", description = "A Backpack", price = 699.99, quantity = 78),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
            return db_product

    return "Product Not Found"


@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return "Product Added Successfully!"


@app.put("/product")
def update_Product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if db_product:
        # db_product.name = product.name
        # db_product.description = product.description
        # db_product.price = product.price
        # db_product.quantity = product.quantity

        update_data = product.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return "Product Updated!"
    else:
        return "No Products Found"


@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return f"Product with Id {id} deleted successfully!"
    else:
        return "Product Not Found"