from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    try:
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except IntegrityError as e:
        db.rollback()  # Rollback the session to avoid incomplete transactions
        raise HTTPException(status_code=500, detail="Database integrity error") from e
    
    except Exception as e:
        db.rollback()  # Rollback the session to avoid incomplete transactions
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

def create_organisation(db: Session, organisation: schemas.OrganisationCreate):
    db_org = models.Organisation(name=organisation.name)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_role_by_id(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_member_by_org_user(db: Session, org_id: int, user_id: int):
    return db.query(models.Member).filter(models.Member.org_id == org_id, models.Member.user_id == user_id).first()

# Add other CRUD operations as needed...
