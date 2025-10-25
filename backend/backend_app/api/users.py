from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.backend_app import database
from backend.backend_app.schemas.user_schema import ContactCreate, ContactOut
from  backend.backend_app.crud import user_crud

router = APIRouter(prefix="/contact", tags=["contact"])

@router.post("/", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(database.get_db)):
    created = await user_crud.create_contact(db, contact)
    return created
