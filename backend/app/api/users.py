# backend/app/api/users.py
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.user_crud import create_contact, get_contacts
from app.schemas.user_schema import ContactCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", tags=["contacts"])
def read_contacts(db: Session = Depends(get_db)):
    return get_contacts(db)

@router.post("/", tags=["contacts"])
def add_contact(name: str = Form(...), email: str = Form(...), message: str = Form(...), db: Session = Depends(get_db)):
    contact_in = ContactCreate(name=name, email=email, message=message)
    contact = create_contact(db, contact_in)
    return contact
