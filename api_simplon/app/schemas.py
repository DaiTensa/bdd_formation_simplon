from pydantic import BaseModel
from typing import Optional


# les classes ci-dessous sont des modèles de données Pydantic
# voir https://pydantic-docs.helpmanual.io/usage/models/
# et https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-automap
# elles sont utilisées pour la validation des données en entrée et en sortie des routes FastAPI
# par exemple, dans la route /formations/{formation_id}, le paramètre formation_id est validé par la classe Formation
# et dans la route /formations/formacode/, les paramètres formacode, skip et limit sont validés par la classe Formations
# pour les sorties, les données retournées par les routes sont validées par les classes Formations et FormationsDept

    

class Formation(BaseModel):
    Id: int
    Libelle: str
    Siret_OF: str
    Simplon_Id: Optional[str] = None
    Resume_Programme: str

    # deprecated
    # class Config:
    #     orm_mode = True
    # orm_mode → from_attributes
    # voir https://docs.pydantic.dev/latest/migration/#changes-to-config

    class Config:
        from_attributes = True

class Formations(BaseModel):
    Id: int
    Libelle: Optional[str] = None
    Siret_OF: str
    Resume_Programme: Optional[str] = None

    class Config:
        from_attributes = True

class FormationsDept(BaseModel):
    Id: int
    Libelle: Optional[str] = None
    Resume_Programme: Optional[str] = None
    Code_Dept: Optional[str] = None

    class Config:
        from_attributes = True
        

class Formacodes(BaseModel):
    Formacode: str
    
    class config:
        from_attributes = True

