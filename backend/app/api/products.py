# backend/app/api/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.product_schema import ProductCreate, Product   # ✅ import đúng schema
from app.crud import product_crud                               # ✅ CRUD đúng module

router = APIRouter()

# Hàm tạo session DB cho mỗi request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📦 Lấy danh sách tất cả sản phẩm
@router.get("/", response_model=list[Product], tags=["products"])
def read_products(db: Session = Depends(get_db)):
    return product_crud.get_products(db)

# 🔍 Lấy thông tin 1 sản phẩm theo ID
@router.get("/{product_id}", response_model=Product, tags=["products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = product_crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ➕ Thêm sản phẩm mới
@router.post("/", response_model=Product, tags=["products"])
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    return product_crud.create_product(db, product_in)

# ❌ Xóa sản phẩm theo ID
@router.delete("/{product_id}", tags=["products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = product_crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Deleted successfully"}
