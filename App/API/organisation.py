from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models, deps

router = APIRouter()

@router.post("/", response_model=schemas.OrganisationResponse)
def create_organisation(organisation: schemas.OrganisationCreate, db: Session = Depends(deps.get_db)):
    return crud.create_organisation(db=db, organisation=organisation)