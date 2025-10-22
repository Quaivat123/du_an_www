from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user_schema import ContactCreate, ContactOut
from app.crud import user_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ContactOut)
def create_contact(contact_in: ContactCreate, db: Session = Depends(get_db)):
    return user_crud.create_contact(db, contact_in)
