from sqlalchemy import Column, ForeignKey, Integer, Enum, String, Date
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


# Primary tables (have associations/relations but are not association tables)
class Organismes(Base):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'organismes'

    # TABLE SPECIFIC COLUMNS
    Nom = Column(String, nullable=True)
    Siret = Column(String, primary_key=True, autoincrement=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy model and use)
    formations = relationship('Formations', back_populates='organisme')


class RNCP_Info(Base):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp_info'

    # TABLE SPECIFIC COLUMNS
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=True)
    Date_Fin = Column(Date, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('RNCP', back_populates='code_rncp')


class RS_Info(Base):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rs_info'

    # TABLE SPECIFIC COLUMNS
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=True)
    Date_Fin = Column(Date, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('RS', back_populates='code_rs')

class NSF_Info(Base):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'nsf_info'

    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('NSF', back_populates='code_nsf')

# Core association tables
class Formations(Base):
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

class Sessions(Base):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'sessions'

    # SPECIFIC TABLE COLUMNS
    Formation_Id = Column(ForeignKey('formations.Id'), nullable=False)
    Code_Session = Column(String, nullable=False)
    Code_Dept = Column(String, nullable=True, server_default='00') # Ususal french dept. number
    Statut = Column(Enum('Active', 'Inactive', name='status_enum'), nullable=False, server_default='Active')

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='sessions')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint('Formation_Id', 'Code_Session', name='session_primary_key'),)


class RNCP(Base):
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

class Formacodes(Base):
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

class Formacodes_Info(Base):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formacodes_info'

    # COMMON COLUMNS OF THE DERIVED TABLES
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('Formacodes', back_populates='formacode')

class RS(Base):
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

class NSF(Base):
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


    
