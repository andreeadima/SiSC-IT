from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ForeignKeyConstraint

Base = declarative_base()

class persoana (Base):
    __tablename__ = "persoana"
    id = Column (Integer, primary_key = True)
    nume = Column (String(45), nullable = False)
    nume_cas = Column (String(45))
    prenume = Column (String(45), nullable = False)
    sex = Column (String(1), nullable = False)
    telefon = Column (String(15), nullable = False)
    e_mail = Column (String(45), nullable = False)
    adresa_fb = Column (String(100), nullable = False)
    adresa_li = Column (String(100), nullable = False)
    domiciliu = Column (String(100), nullable = False)
    statut = Column (String(45), nullable = False)

    licente = relationship ("licenta", backref = "persoana")
    mastere = relationship ("master", backref = "persoana")
    doctorate = relationship ("doctorat", backref = "persoana")
    jobs = relationship ("job", backref = "persoana")
    

class licenta (Base):
    __tablename__ = "licenta"
    id = Column (Integer, primary_key = True)
    universitate = Column (String(45), nullable = False)
    facultate = Column (String(100), nullable = False)
    specializare = Column (String(100))
    an_inm = Column (Integer, nullable = False)
    an_abs = Column (Integer, nullable = False)

    idpersoana = Column (Integer, ForeignKey('persoana.id', onupdate="CASCADE", ondelete="CASCADE"))
    

class master (Base):
    __tablename__ = "master"
    id = Column (Integer, primary_key = True)
    universitate = Column (String(45), nullable = False)
    facultate = Column (String(100), nullable = False)
    specializare = Column (String(100), nullable = False)
    an_inm = Column (Integer, nullable = False)
    an_abs = Column (Integer, nullable = False)

    idpersoana = Column (Integer, ForeignKey('persoana.id', onupdate="CASCADE", ondelete="CASCADE"))

class doctorat (Base):
    __tablename__ = "doctorat"
    id = Column (Integer, primary_key = True)
    universitate = Column (String(45), nullable = False)
    domeniu = Column (String(100), nullable = False)
    an = Column (Integer, nullable = False)
    idpersoana = Column (Integer, ForeignKey('persoana.id', onupdate="CASCADE", ondelete="CASCADE"))

class job (Base):
    __tablename__ = "job"
    id = Column (Integer, primary_key = True)
    post = Column (String(45), nullable = False)
    perioada = Column (String(45))
    companie = Column (String(100))
    domeniu = Column (String(45), nullable = False)
    localitate = Column (String(100), nullable = False)
    numar_angajati = Column (String(45), nullable = False)
    job_anterior = Column (String(100), nullable = False)
                         
    idpersoana = Column (Integer, ForeignKey('persoana.id', onupdate="CASCADE", ondelete="CASCADE"))
    

engine = create_engine('mysql+mysqlconnector://root:@localhost/formular', echo = False)
Base.metadata.create_all(engine)

    
    
