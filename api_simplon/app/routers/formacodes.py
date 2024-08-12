from fastapi import APIRouter, Depends, HTTPException, Path , Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from typing import List


router = APIRouter()

@router.get("/distinct_formacodes/", response_model=List[schemas.Formacodes])
def read_distinct_formacodes(db: Session = Depends(get_db)):
    """
    Retrieve a list of distinct formacodes.

    Args:
        db (Session): The database session.

    Returns:
        List[Formacodes]: The list of distinct formacodes.
    """
    formacodes_distinct = crud.get_distinct_formacodes(db)
    return [schemas.Formacodes.model_validate(formacode) for formacode in formacodes_distinct]