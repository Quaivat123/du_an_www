from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.backend_app.models.user_model import Contact
from backend.backend_app.schemas.user_schema import ContactUpdate
# Lấy tất cả contact
async def get_all_contacts(db: AsyncSession):
    result = await db.execute(select(Contact))
    return result.scalars().all()

# Lấy contact theo ID
async def get_contact_by_id(db: AsyncSession, customer_id: int):
    result = await db.execute(select(Contact).filter(Contact.id == customer_id))
    return result.scalar_one_or_none()

# Cập nhật contact
async def update_contact(db: AsyncSession, customer_id: int, contact_update: ContactUpdate):
    db_contact = await get_contact_by_id(db, customer_id)
    if db_contact:
        update_data = contact_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        await db.commit()
        await db.refresh(db_contact)
    return db_contact

# Xóa contact
async def delete_contact(db: AsyncSession, customer_id: int):
    db_contact = await get_contact_by_id(db, customer_id)
    if db_contact:
        await db.delete(db_contact)
        await db.commit()
    return db_contact