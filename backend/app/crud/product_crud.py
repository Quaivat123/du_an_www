from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import ProductCreate

def create_product(db: Session, product_in: ProductCreate):
    product = Product(**product_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session):
    return db.query(Product).order_by(Product.id.desc()).all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False
