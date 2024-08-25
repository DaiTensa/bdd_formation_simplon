from sqlalchemy import Column, ForeignKey, Integer, Enum
from sqlalchemy import String, Date, Numeric, Boolean
from sqlalchemy import create_engine, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import relationship, declared_attr, column_property
from dotenv import load_dotenv
load_dotenv()

import os
import urllib.parse

# INSTANCIATING A DATABASE FRAMEWORK (i.e. a mix of container and base class) 
SimplonDB = declarative_base()

def get_connection_uri():
    # Read URI parameters from the environment or use default values
    dbhost = os.getenv('DBHOST', 'localhost')  # Default to 'localhost'
    dbname = os.getenv('DBNAME', 'mydatabase')  # Default database name
    dbuser = urllib.parse.quote(os.getenv('DBUSER', 'myuser'))  # Default user
    password = urllib.parse.quote(os.getenv('PASSWORD', 'mypassword'))  # Default password

    # Create the connection URI
    db_uri = f"postgresql://{dbuser}:{password}@{dbhost}/{dbname}"
    return db_uri

if os.getenv('DB_SQLITE') == 'True':
    URL_DATA_BASE = 'sqlite:///../simplon.db'
else:
    URL_DATA_BASE = get_connection_uri()


def db_connect(url: str = URL_DATA_BASE, **kwargs):
    """
    Creates or updates the database schema then returns access to it.

    The database itself is never overwritten but only udpdated or created when
    not already in place. The same for the tables inside the database.

    Parameter(s):
        url (str): url to connect the choosen database.
                   By default: "sqlite:///../simplon.db"
        **kwargs : Additional arguments to be passed to `create_engine` method.
                   For any details about the said method, see SQLAlchemy doc.
                   Example: It is possible

    Returns:
        A SQLAlchemy `sessionmaker` object to be instanciated into sessions.
    """
    # SET THE DB TYPE (sqlite, PostgreSQL, etc.) AND AN ENGINE (i.e. connector)
    engine = create_engine(url, **kwargs)

    # CREATES THE REQUIRED DATABASE (according data given into `url`)
    
    SimplonDB.metadata.create_all(engine, checkfirst=True)

    # FUNCTION OUTPUT (returns a `sessionmaker` object to help DB interactions)
    return sessionmaker(bind=engine)

# CREATING TABLES OF THE DATABASE
# Primary tables (have associations/relations but are not association tables)
class Organismes(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'organismes'

    # TABLE SPECIFIC COLUMNS
    Nom = Column(String, nullable=True)
    Siret = Column(String, primary_key=True, autoincrement=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy model and use)
    formations = relationship('Formations', back_populates='organisme')

# class Codes_Info(SimplonDB): # Abstract table (code factorization purpose)
#     """
#     Almost ready-to-use table for all code "Info" tables.

#     Helps factorizing code as it is a common part of some other sub classes
#     """
#     # RAW PARAMETERS AND SETINGS
#     __abstract__ = True

#     # COMMON COLUMNS OF THE DERIVED TABLES
#     Code = Column(String, primary_key=True, autoincrement=False)
#     Libelle = Column(String, nullable=True)

class RNCP_Info(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp_info'

    # TABLE SPECIFIC COLUMNS
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=True)
    Date_Fin = Column(Date, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('RNCP', back_populates='code_rncp')


class RS_Info(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rs_info'

    # TABLE SPECIFIC COLUMNS
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=True)
    Date_Fin = Column(Date, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('RS', back_populates='code_rs')

class NSF_Info(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'nsf_info'

    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('NSF', back_populates='code_nsf')

# Core association tables
class Formations(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formations'

    # TABLE SPECIFIC COLUMNS
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Libelle = Column(String, nullable=False)
    Siret_OF = Column(ForeignKey('organismes.Siret'), nullable=False)
    Simplon_Id = Column(String, nullable=True)
    Resume_Programme = Column(String, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy model and use)
    codes_rs = relationship('RS', back_populates='formation')
    sessions = relationship('Sessions', back_populates='formation')
    codes_nsf = relationship('NSF', back_populates='formation')
    organisme = relationship('Organismes', back_populates='formations')
    formacodes = relationship('Formacodes', back_populates='formation')
    codes_rncp = relationship('RNCP', back_populates='formation')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (UniqueConstraint('Libelle', 'Siret_OF', name='Libelle+Siret_OF_is_unique!'),)

class Sessions(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'sessions'

    # SPECIFIC TABLE COLUMNS
    Formation_Id = Column(ForeignKey('formations.Id'), nullable=False)
    Code_Session = Column(String, nullable=False)
    Code_Dept = Column(String, nullable=True, server_default='00') # Ususal french dept. number
    Statut = Column(Enum('Active', 'Inactive', name='status_enum'), nullable=False, server_default='Active')
    # Ville = Column(String, nullable=True)
    # Nom_Dept = Column(String, nullable=True)
    # Nom_Region = Column(String, nullable=True)
    # Code_Region = Column(String, nullable=True)
    # Date_Debut = Column(Date, nullable=True)
    # Date_Lim_Cand = Column(Date, nullable=True)
    # Duree = Column(String, nullable=True)
    # Alternance = Column(Integer, nullable=False, server_default='0')
    # Distanciel = Column(Integer, nullable=False, server_default='0')
    # Niveau_Sortie = Column(String, nullable=True)
    # Libelle_Session = Column(String, nullable=True)
    
    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='sessions')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint('Formation_Id', 'Code_Session', name='session_primary_key'),)
    # __table_args__ = (PrimaryKeyConstraint(*('Formation_Id', 'Code_Session'),
    #                                        name='Composite_primary_key'),)

# # Secondary association tables
# class Codes_Formations(SimplonDB): # Abstract table (for code factorization)
#     """
#     Almost ready-to-use table for associations between codes and trainings.

#     Helps factorizing code as it is a common part of some other sub classes.
#     """
#     # RAW PARAMETERS AND SETINGS
#     __abstract__ = True

#     # COMMON COLUMNS OF THE DERIVED TABLES
#     Formation_Id = Column(*foreign_key('formations.Id'), nullable=False)

class RNCP(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp'

    # TABLE COLUMNS
    Formation_Id = Column(ForeignKey('formations.Id'), nullable=False)
    Code_RNCP = Column(ForeignKey('rncp_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='codes_rncp')
    code_rncp = relationship('RNCP_Info', back_populates='formations')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint('Formation_Id', 'Code_RNCP', name='rncp_primary_key'),)

class Formacodes(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formacodes'

    # TABLE COLUMNS
    Formation_Id = Column(ForeignKey('formations.Id'), nullable=False)
    Formacode = Column(ForeignKey('formacodes_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='formacodes')
    formacode = relationship('Formacodes_Info', back_populates='formations')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint('Formation_Id', 'Formacode', name='formacodes_primary_key'),)

class Formacodes_Info(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formacodes_info'

    # COMMON COLUMNS OF THE DERIVED TABLES
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('Formacodes', back_populates='formacode')

class RS(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rs'

    # TABLE COLUMNS
    Formation_Id = Column(ForeignKey('formations.Id'), nullable=False)
    Code_RS = Column(ForeignKey('rs_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='codes_rs')
    code_rs = relationship('RS_Info', back_populates='formations')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint('Formation_Id', 'Code_RS', name='rs_primary_key'),)

class NSF(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'nsf'

    # TABLE COLUMNS
    Formation_Id = Column(ForeignKey('formations.Id'), nullable=False)
    Code_NSF = Column(ForeignKey('nsf_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='codes_nsf')
    code_nsf = relationship('NSF_Info', back_populates='formations')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint('Formation_Id', 'Code_NSF', name='nsf_primary_key'),)


    
