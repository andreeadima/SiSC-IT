from flask import Flask, request, json, jsonify, Response
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ForeignKeyConstraint, CheckConstraint, update

Base = declarative_base()

class Persoana (Base):
    __tablename__ = "Persoana"
    id = Column (Integer, primary_key = True)
    nume = Column (String(45), nullable = False)
    nume_cas = Column (String(45))
    prenume = Column (String(45), nullable = False)
    sex = Column (String(1), nullable = False)
    telefon = Column (String(15), nullable = False) #telefonul nu e integer deoarece exista posibilitatea numerelor de tip +407...
    e_mail = Column (String(45), nullable = False)
    adresa_fb = Column (String(100), nullable = False)
    adresa_li = Column (String(100), nullable = False)
    domiciliu = Column (String(100), nullable = False)
    statut = Column (String(45), nullable = False)

    licente = relationship ("Licenta", backref = "Persoana")
    mastere = relationship ("Master", backref = "Persoana")
    doctorate = relationship ("Doctorat", backref = "Persoana")
    jobs = relationship ("Job", backref = "Persoana")

    @property
    def serialize(self):
        return {
        "id": self.id,
        "nume": self.nume,
        "nume_cas": self.nume_cas,
        "prenume" : self.prenume,
        "sex" : self.sex,
        "telefon" : self.telefon,
        "e_mail" : self.e_mail,
        "adresa_fb" : self.adresa_fb,
        "adresa_li" : self.adresa_li,
        "domiciliu" : self.domiciliu,
        "statut" : self.statut
        }    


class Licenta (Base):
    __tablename__ = "Licenta"
    id = Column (Integer, primary_key = True)
    universitate = Column (String(45), nullable = False)
    facultate = Column (String(100), nullable = False)
    specializare = Column (String(100))
    an_inm = Column (Integer, nullable = False)
    an_abs = Column (Integer, nullable = False)

    CheckConstraint('an_abs > an_inm', name='check1')
    CheckConstraint('an_abs > 1900', name='check2')
    CheckConstraint('an_abs < 2300', name='check3')

    idpersoana = Column (Integer, ForeignKey('Persoana.id', onupdate="CASCADE", ondelete="CASCADE"))

    @property
    def serialize(self):
        return {
        "id": self.id,
        "universitate": self.universitate,
        "facultate" : self.facultate,
        "specializare" : self.specializare,
        "an_inm" : self.an_inm,
        "an_abs" : self.an_abs
        }
    

class Master (Base):
    __tablename__ = "Master"
    id = Column (Integer, primary_key = True)
    universitate = Column (String(45), nullable = False)
    facultate = Column (String(100), nullable = False)
    specializare = Column (String(100), nullable = False)
    an_inm = Column (Integer, nullable = False)
    an_abs = Column (Integer, nullable = False)

    CheckConstraint('an_abs > an_inm', name='check4')
    CheckConstraint('an_abs > 1900', name='check5')
    CheckConstraint('an_abs < 2300', name='check6')
    

    idpersoana = Column (Integer, ForeignKey('Persoana.id', onupdate="CASCADE", ondelete="CASCADE"))

    @property
    def serialize(self):
        return {
        "id": self.id,
        "universitate": self.universitate,
        "facultate" : self.facultate,
        "specializare" : self.specializare,
        "an_inm" : self.an_inm,
        "an_abs" : self.an_abs
    }

class Doctorat (Base):
    __tablename__ = "Doctorat"
    id = Column (Integer, primary_key = True)
    universitate = Column (String(45), nullable = False)
    domeniu = Column (String(100), nullable = False)
    an = Column (Integer, nullable = False)
    idpersoana = Column (Integer, ForeignKey('Persoana.id', onupdate="CASCADE", ondelete="CASCADE"))

    CheckConstraint('an > 1900', name='check7')
    CheckConstraint('an < 2300', name='check8')

    @property
    def serialize(self):
        return {
    	"id": self.id,
    	"universitate": self.universitate,
        "facultate" : self.facultate,
        "domeniu" : self.domeniu,
        "an" : self.an
    }

class Job (Base):
    __tablename__ = "Job"
    id = Column (Integer, primary_key = True)
    post = Column (String(45), nullable = False)
    perioada = Column (String(45))
    companie = Column (String(100))
    domeniu = Column (String(45), nullable = False)
    localitate = Column (String(100), nullable = False)
    numar_angajati = Column (String(45), nullable = False)
    job_anterior = Column (String(100), nullable = False)
                         
    idpersoana = Column (Integer, ForeignKey('Persoana.id', onupdate="CASCADE", ondelete="CASCADE"))
    
    @property
    def serialize(self):
        return {
    	"id": self.id,
    	"post": self.universitate,
    	"perioada" : self.facultate,
        "companie" : self.companie,
        "domeniu" : self.domeniu,
        "localitate" : self.localitate,
        "numar_angajati" : self.numar_angajati,
        "job_anterior" : self.job_anterior
    }
engine = create_engine('mysql+mysqlconnector://root:@localhost/formular', echo = False)
Base.metadata.create_all(engine)

print ("Creat baza de date")

Session = sessionmaker(bind=engine)
session = Session()


app = Flask(__name__)
app.debug = True

@app.route("/something", methods=['GET'])
def get_info ():
        pers = (session.query(Persoana, Licenta, Master, Doctorat, Job).join(Licenta).join(Master).join(Doctorat).join(Job)).all()
        r = Response(json.dumps([ob.serialize for ob in pers]), status=200, mimetype='application/json')
        return r
    
@app.route("/something/<int:Persoana.id>", methods=['DELETE'])
def delete(Persoana_id):
        pers = session.query(Persoana).filter(Persoana.id == Persoana_id).one()
        session.delete(pers)
        session.commit()
        r = Response(json.dumps([pers.serialize]), status=200, mimetype='application/json')
        return r
    
@app.route("/something/<int:Persoana_id>", methods=['PUT'])
def modif_pers(persoana_id):
        data = request.get_json()
        pers = session.query(Persoana).filter(Persoana.id == persoana_id).one()

        pers.nume = data["nume"] 
        pers.nume_cas = data["nume_cas"]
        pers.prenume = data["prenume"]
        pers.sex = data["sex"]
        pers.telefon = data["telefon"] 
        pers.e_mail = data["e_mail"]
        pers.adresa_fb = data["adresa_fb"]
        pers.adresa_li = data["adresa_li"]
        pers.domiciliu = data["domiciliu"]
        pers.statut = data["statut"]
        session.add(pers)
        
        session.commit()

        licenta = session.query(Licenta).filter(Licenta.idpersoana == persoana_id).all()
        for ob in licenta :
            ob.id = data["id"]
            ob.universitate = data["universitate"]
            ob.facultate = data["facultate"]
            ob.specializare = data["specializare"] 
            ob.an_inm = data["an_inm"] 
            ob.an_abs = data["an_abs"]
            session.add(ob)
            
        session.commit()

        master = session.query(Master).filter(Master.idpersoana == persoana_id).all()
        for ob in master :
            ob.id = data["id"]
            ob.universitate = data["universitate"]
            ob.facultate = data["facultate"]
            ob.specializare = data["specializare"] 
            ob.an_inm = data["an_inm"] 
            ob.an_abs = data["an_abs"]
            session.add(ob)

        session.commit()
        
        doctorat = session.query(Doctorat).filter(Doctorat.idpersoana == persoana_id).one()
        
        doctorat.id = data["id"]
        doctorat.universitate = data["universitate"]
        doctorat.facultate = data["facultate"] 
        doctorat.domeniu = data["domeniu"] 
        doctorat.an = data["an"]

        session.add(doctorat)
        session.commit()


        job = session.query(Job).filter(Job.idpersoana == persoana_id).all()
        
        for ob in job:
            ob.id = data["id"]
            ob.post = data["post"]
            ob.perioada = data["perioada"]
            ob.companie = data["companie"] 
            ob.domeniu = data["domeniu"]
            ob.localitate = data["localitate"]
            ob.numar_angajati = data["numar_angajati"] 
            ob.job_anterior = data["job_anterior"]
            session.add(ob)

        session.commit()

        r = Response(json.dumps([pers.serialize],[ob.serialize for ob in licenta], [ob.serialize for ob in master], [doctorat.serialize], [ob.serialize for ob in job]), status=201, mimetype='application/json')
        return r
    
@app.route("/something", methods=['POST'])
def add_person():
	data = request.get_json()
	pers = Persoana(nume = data["nume"], nume_cas = data["nume_cas"], prenume = data["prenume"], sex = data["sex"], telefon = data["telefon"], e_mail = data["e_mail"], adresa_fb = data["adresa_fb"], adresa_li = data["adresa_li"], domiciliu = data["domiciliu"], statut = data["statut"])
	session.add(pers)
	session.commit()
	licenta = Licenta(universitate = data["universitate"], facultate = data["facultate"], specializare = data["specializare"], an_inm = data["an_inm"], an_abs = data["an_abs"])
	session.add(licenta)
	session.commit()
	master = Master(universitate = data["universitate"], facultate = data["facultate"], specializare = data["specializare"], an_inm = data["an_inm"], an_abs = data["an_abs"])
	session.add(master)
	session.commit()
	doctorat = Doctorat(universitate = data["universitate"], facultate = data["facultate"], domeniu = data["domeniu"], an = data["an"])
	session.add(doctorat)
	session.commit()
	job = Job(post = data["post"], perioada = data["perioada"], companie = data["companie"], domeniu = data["domeniu"], localitate = data["localitate"], numar_angajati = data["numar_angajati"] , job_anterior = data["job_anterior"])
	session.add(job)
	session.commit()
	r = Response(json.dumps(pers.serialize), status=201, mimetype='application/json')
	return r
    
if __name__ == "__main__":
    app.run()

    
    
