from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models, deps

router = APIRouter()

@router.post("/", response_model=schemas.RoleResponse)
def create_role(role: schemas.RoleCreate, db: Session = Depends(deps.get_db)):
    return crud.create_role(db=db, role=role)