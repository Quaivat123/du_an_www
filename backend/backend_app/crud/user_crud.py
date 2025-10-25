# backend/backend_app/crud/user_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.backend_app.models.user_model import Contact
from backend.backend_app.schemas.user_schema import ContactCreate
from .. import models,schemas
async def create_contact(db: AsyncSession, contact_in: schemas.user_schema.ContactCreate):
    db_contact = models.user_model.Contact(**contact_in.model_dump())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact


# async def get_contacts(db: AsyncSession):
#     return db.query(Contact).order_by(Contact.id.desc()).all()
