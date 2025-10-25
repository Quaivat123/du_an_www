# backend/backend_app/api/products.py
from fastapi import APIRouter, Depends, HTTPException
from backend.backend_app.database import get_db
from backend.backend_app.database import AsyncSession
from backend.backend_app.schemas.product_schema import ProductCreate, Product   # ✅ import đúng schema
from backend.backend_app.crud import product_crud                               # ✅ CRUD đúng module

router = APIRouter()


# 📦 Lấy danh sách tất cả sản phẩm
@router.get("/", response_model=list[Product], tags=["products"])
async def read_products(db: AsyncSession = Depends(get_db)):
    return await product_crud.get_products(db)

# 🔍 Lấy thông tin 1 sản phẩm theo ID
@router.get("/{product_id}", response_model=Product, tags=["products"])
def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = product_crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ➕ Thêm sản phẩm mới
@router.post("/", response_model=Product, tags=["products"])
def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    return product_crud.create_product(db, product_in)

# ❌ Xóa sản phẩm theo ID
@router.delete("/{product_id}", tags=["products"])
def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    ok = product_crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Deleted successfully"}
