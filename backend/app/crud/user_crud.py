# backend/app/crud/user_crud.py
from sqlalchemy.orm import Session
from app.models.user import Contact
from app.schemas.user_schema import ContactCreate

# def create_contact(db: Session, contact: ContactCreate):
#     db_contact = Contact(name=contact.name, email=contact.email, message=contact.message)
#     db.add(db_contact)
#     db.commit()
#     db.refresh(db_contact)
#     return db_contact
def create_contact(db: Session, contact_in: ContactCreate):
    db_contact = Contact(**contact_in.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session):
    return db.query(Contact).order_by(Contact.id.desc()).all()
