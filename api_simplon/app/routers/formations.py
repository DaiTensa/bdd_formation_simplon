from fastapi import APIRouter, Depends, HTTPException, Path , Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from typing import List


router = APIRouter()


@router.get("/")
def read_root():
    """home page

    Returns:
    - **200 OK**: Bienvenue sur l'API Simplon
    """
    return "Bienvenue sur l'API Simplon"


@router.get("/formations/{formation_id}", response_model=schemas.Formation)
def read_formation(
    formation_id: int = Path(..., description="L'Id d'une formation.", example="150"), 
    db: Session = Depends(get_db)):
    """
    Récupère les détails d'un formation en fonction de l'Id fourni.

    - **formation_id**: L'Id d'une fromation.

    Réponses:
    - **200 OK**: Retourne une  formations.
    - **404 Not Found**: Si aucune formation n'est trouvée pour l'Id fourni.
    """
    db_formation = crud.get_formation_by_id(db, formation_id=formation_id)
    if db_formation is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    return schemas.Formation.model_validate(db_formation)

# Get formations by formacode
@router.get("/formations/formacode/", response_model=List[schemas.Formations])
def read_formations_by_formacode(

    formacode: List[str] = Query(..., 
                                 description="Liste des codes formacode pour filtrer les formations.",
                                 example="15052"), 

    skip: int = Query(0, alias="offset", 
                      description="Nombre de résultats à sauter (par défaut 0)."), 

    limit: int = Query(10, le=100, 
                       description="Nombre maximum de résultats à retourner (par défaut 10, maximum 100)."),

    db: Session = Depends(get_db)):

    """
    Récupère une liste de formations en fonction des codes formacode fournis.

    - **formacode**: Liste des codes formacode pour filtrer les formations.
    - **offset**: Nombre de résultats à sauter (par défaut 0).
    - **limit**: Nombre maximum de résultats à retourner (par défaut 10, maximum 100).

    Réponses:
    - **200 OK**: Retourne une liste de formations.
    - **404 Not Found**: Si aucune formation n'est trouvée pour les codes formacode fournis.
    """

    db_formations = crud.get_formations_by_formacode(db, formacode=formacode, skip=skip, limit=limit)
    if db_formations is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    return [schemas.Formations.model_validate(formation) for formation in db_formations]

# Get formations by department
@router.get("/formations/department/", response_model=List[schemas.FormationsDept])
def read_formations_by_department(

    department: List[str] = Query(..., 
                                  description="Liste des départements pour filtrer les formations.",
                                  example="75"), 

    skip: int = Query(0, alias="offset", 
                      description="Nombre de résultats à sauter (par défaut 0)."), 

    limit: int = Query(10, le=100, 
                       description="Nombre maximum de résultats à retourner (par défaut 10, maximum 100)."),

    db: Session = Depends(get_db)):

    """
    Récupère une liste de formations en fonction des départements fournis.

    - **department**: Liste des départements pour filtrer les formations.
    - **offset**: Nombre de résultats à sauter (par défaut 0).
    - **limit**: Nombre maximum de résultats à retourner (par défaut 10, maximum 100).

    Réponses:
    - **200 OK**: Retourne une liste de formations.
    - **404 Not Found**: Si aucune formation n'est trouvée pour les départements fournis.
    """

    db_formations_dept = crud.get_formations_by_department(db, department=department, skip=skip, limit=limit)
    if db_formations_dept is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    return [schemas.FormationsDept.model_validate(formation) for formation in db_formations_dept]

