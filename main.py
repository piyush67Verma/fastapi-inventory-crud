from fastapi import FastAPI, Depends
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*']
)
#  Below line creates tables for the class
#  which inherits Base class of the sqlalchemy
database_models.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


products = [
    Product(id=10, name='Laptop', description="Lenovo laptop", price=1000, quantity=5),
    Product(id=210, name='Smartphone', description="Samsung", price=500, quantity=10),
    Product(id=350, name='Keyboard', description="Logitech", price=100, quantity=20)
]


def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        
        db.commit()


init_db()

@app.get("/home")
def greet():
    return "Welcome to the world of FastAPI"

@app.get("/products")
def getAllProducts(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        return db_product
    
    return "Product not found"

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id:int, product:Product, db: Session = Depends(get_db)):

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product found"
    
    return "Product Not found"
    

@app.delete("/products/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
       db.delete(db_product)
       db.commit()
       return "Product Deleted"

    return "Product Not found"


