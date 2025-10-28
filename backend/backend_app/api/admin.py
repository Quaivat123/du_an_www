from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError

from backend.backend_app.core.config import settings
from backend.backend_app.core.security import verify_password
from backend.backend_app.database import get_db
from backend.backend_app.schemas.admin_schema import AdminLogin
from backend.backend_app.schemas.user_schema import ContactUpdate
from backend.backend_app.models.admin_model import Admin
from backend.backend_app.models.user_model import Contact

# ============ Router Configuration ============
router = APIRouter(prefix="/admin", tags=["Admin"])
bearer_scheme = HTTPBearer()

# ============ JWT Token ============
def create_access_token(data: dict) -> str:
    """Tạo JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> str:
    """Xác thực và lấy thông tin user từ token"""
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )

# ============ Admin Authentication ============
@router.post("/login")
async def admin_login(form_data: AdminLogin, db: AsyncSession = Depends(get_db)):
    """Đăng nhập admin"""
    result = await db.execute(select(Admin).filter(Admin.username == form_data.username))
    admin = result.scalar_one_or_none()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tài khoản hoặc mật khẩu"
        )

    # Kiểm tra password
    if not verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tài khoản hoặc mật khẩu"
        )

    access_token = create_access_token({"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ============ Contact Management APIs ============
@router.get("/contacts")
async def get_all_contacts(
    db: AsyncSession = Depends(get_db),
    _current_user: str = Depends(get_current_user)  # Chỉ để xác thực, không dùng trực tiếp
):
    """Lấy danh sách tất cả contacts"""
    result = await db.execute(select(Contact).order_by(Contact.created_at.desc()))
    return result.scalars().all()

@router.get("/contacts/{contact_id}")
async def get_contact_by_id(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: str = Depends(get_current_user)
):
    """Lấy chi tiết một contact"""
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(status_code=404, detail="Không tìm thấy contact")

    return contact

@router.put("/contacts/{contact_id}")
async def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: str = Depends(get_current_user)
):
    """Cập nhật thông tin contact"""
    # Tìm contact
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(status_code=404, detail="Không tìm thấy contact")

    # Cập nhật các trường được gửi lên
    update_data = contact_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)

    await db.commit()
    await db.refresh(contact)

    return contact

@router.delete("/contacts/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: str = Depends(get_current_user)
):
    """Xóa contact"""
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(status_code=404, detail="Không tìm thấy contact")

    await db.delete(contact)
    await db.commit()

    return {"message": "Xóa contact thành công", "id": contact_id}
