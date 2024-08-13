from sqlalchemy.orm import Session
from . import models

# this file contains the CRUD (Create, Read, Update, Delete) operations for the database

def get_formation_by_id(db: Session, formation_id: int):
    """
    Retrieve a formation by its ID.

    Args:
        db (Session): The database session.
        formation_id (int): The ID of the formation.

    Returns:
        Formation: The formation with the specified ID, if found. Otherwise, None.
    """
    return (
        db.query(models.Formations)
        .filter(models.Formations.Id == formation_id)
        .first())

def get_formations_by_formacode(db: Session, formacode: list, skip: int = 0, limit: int = 10):
    """
    Retrieve formations by their formacodes.

    Args:
        db (Session): The database session.
        formacode (list): The list of formacodes.
        skip (int, optional): The number of formations to skip. Defaults to 0.
        limit (int, optional): The maximum number of formations to retrieve. Defaults to 10.

    Returns:
        List[Formation]: The list of formations with the specified formacodes.
    """
    return (
        db.query(models.Formations)
        .join(models.Formacodes)
        .filter(models.Formacodes.Formacode.in_(formacode))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_formations_by_department(db: Session, department: list, skip: int = 0, limit: int = 10):
    """
    Retrieve formations by their department.

    Args:
        db (Session): The database session.
        department (list): The list of departments.
        skip (int, optional): The number of formations to skip. Defaults to 0.
        limit (int, optional): The maximum number of formations to retrieve. Defaults to 10.

    Returns:
        List[Formation]: The list of formations in the specified departments.
    """
    results = (db.query(models.Formations, models.Sessions.Code_Dept)
        .join(models.Sessions)
        .filter(models.Sessions.Code_Dept.in_(department))
        .offset(skip)
        .limit(limit)
        .all())
    
    formations_with_dept = [
        {
            "Id": result[0].Id,
            "Libelle": result[0].Libelle,
            "Resume_Programme": result[0].Resume_Programme,
            "Code_Dept": result[1]
        }
        for result in results
    ]
    return formations_with_dept

def get_distinct_formacodes(db: Session):
    """
    Retrieve distinct formacodes.

    Args:
        db (Session): The database session.

    Returns:
        List[str]: The list of distinct formacodes.
    """
    formacodes = (
        db.query(models.Formacodes.Formacode)
        .distinct()
        .all()
    ) 
    return [{"Formacode": formacode[0]} for formacode in formacodes]