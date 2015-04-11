from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Float
from flask import Flask, json, Response, request

Base = declarative_base()


class OptionS(Base):
    __tablename__ = "option_s"
    os_id = Column(Integer, primary_key=True)
    os_lastupdate = Column(TIMESTAMP)
    os_form_id = Column(Integer, ForeignKey("form.f_id", ondelete="CASCADE", onupdate="CASCADE"))
    os_student_id = Column(Integer, ForeignKey("student.s_id"))


class OptionD(Base):
    __tablename__ = "option_d"
    od_id = Column(Integer, primary_key=True)
    od_lastupdate = Column(TIMESTAMP)
    od_form_id = Column(Integer, ForeignKey("form.f_id", ondelete="CASCADE", onupdate="CASCADE"))
    od_dorm_id = Column(Integer, ForeignKey("dorm.d_id"))


class RoomStudent(Base):
    __tablename__ = "room_student"
    rs_id = Column(Integer, primary_key=True)
    rs_lastupdate = Column(TIMESTAMP)
    rs_room_id = Column(Integer, ForeignKey("room.r_id", onupdate="CASCADE"))
    rs_student_id = Column(Integer, ForeignKey("student.s_id", onupdate="CASCADE"))


class Room(Base):
    __tablename__ = "room"
    r_id = Column(Integer, primary_key=True)
    r_nr = Column(Integer)
    r_spaces = Column(Integer)
    r_status = Column(String(20))
    r_dorm_id = Column(Integer, ForeignKey('dorm.d_id'))

    room_stud = relationship("RoomStudent", backref="room")

    @property
    def serialize(self):
        return {
            "Room_nr": self.r_nr,
            "Room_size": self.r_spaces,
            "Room_status": self.r_status,
            "Dorm_id": self.r_dorm_id
        }


class Form(Base):
    __tablename__ = "form"
    f_id = Column(Integer, primary_key=True)
    f_lastupdate = Column(TIMESTAMP)
    f_student_id = Column(Integer, ForeignKey("student.s_id"))

    form_option_d = relationship("OptionD", backref="form")
    form_option_s = relationship("OptionS", backref="form")

    @property
    def serialize(self):
        return {
            "Student": self.f_student_id
        }


class Dorm(Base):
    __tablename__ = "dorm"
    d_id = Column(Integer, primary_key=True)
    d_name = Column(String(50))

    room = relationship("Room", backref="dorm")
    dorm_option = relationship("OptionD", backref="dorm")

    @property
    def serialize(self):
        return {
            "Dorm_name": self.d_name
        }


class Student(Base):
    __tablename__ = "student"
    s_id = Column(Integer, primary_key=True)
    s_fname = Column(String(45))
    s_lname = Column(String(45))
    s_medie = Column(Float)

    student_room = relationship("RoomStudent", backref="student")
    option_student = relationship("OptionS", backref="student")
    form = relationship("Form", uselist=False, backref="student")

    @property
    def serialize(self):
        return {
            "First_name": self.s_fname,
            "Last_name": self.s_lname,
            "Grade": self.s_medie
        }


engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/camine', echo=False)

print("Works!")

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.debug = True


@app.route("/dorm", methods=['GET'])
def get_dorm():
    dorms = session.query(Dorm).all()
    response = Response(json.dumps([ob.serialize for ob in dorms]), status=200, mimetype="application/json")
    return response


@app.route("/room/<int:dorm_id>", methods=['GET'])
def get_rooms(dorm_id):
    rooms = session.query(Room).join(Dorm).filter(Dorm.d_id == dorm_id).all()
    response = Response(json.dumps([item.serialize for item in rooms]), status=200, mimetype="application/json")
    return response


@app.route("/room/<string:oldstud_id>/<string:newstud_id>", methods=['PUT'])
def replace_stud(oldstud_id, newstud_id):
    record = session.query(RoomStudent).join(Student).filter(Student.s_id == oldstud_id).one()
    session.add(record)
    record.rs_student_id = newstud_id
    session.commit()
    response = Response(json.dumps("Worked!"), status=200, mimetype="application/json")
    return response


@app.route("/students", methods=['GET'])
def get_stud():
    students = session.query(Student).all()
    response = Response(json.dumps([item.serialize for item in students]), status=200, mimetype="application/json")
    return response


@app.route("/form", methods=['GET'])
def get_form():
    forms = session.query(Form).all()
    dictionary = dict()
    for item in forms:
        student = session.query(Student).join(Form).filter(Student.s_id == item.f_student_id).one()
        dorms = session.query(Dorm).join(OptionD).join(Form).filter(Form.f_id == item.f_id).all()
        roomates = session.query(Student).join(OptionS).join(Form).filter(Form.f_id == item.f_id).all()
        dictionary["Student first name"] = student.s_fname
        dictionary["Student last name"] = student.s_lname
        i = 1
        for dorm_item in dorms:
            dictionary["Dorm" + str(i) + " name"] = dorm_item.d_name
            i += 1
        i = 1
        for student_item in roomates:
            dictionary["Roommate" + str(i) + " first name"] = student_item.s_fname
            dictionary["Roommate" + str(i) + " last name"] = student_item.s_lname
            dictionary["Roommate" + str(i) + " grade"] = student_item.s_medie
            i += 1
    response = json.dumps(dictionary)
    return Response(response, status=200, mimetype="application/json")


@app.route("/new-form", methods=['POST'])
def new_form():
    data = request.get_json()
    student = session.query(Student).filter(Student.s_id == data["Student_id"]).one()
    form = Form(f_student_id=student.s_id)
    session.add(form)
    session.commit()
    if data["Roommates"]:
        for item in data["Roommates"]:
            student = session.query(Student).filter(Student.s_id == item).one()
            option = OptionS(os_form_id=form.f_id, os_student_id=student.s_id)
            session.add(option)
            session.commit()
    if data["Dorms"]:
        for item in data["Dorms"]:
            dorm = session.query(Dorm).filter(Dorm.d_id == item).one()
            option = OptionD(od_form_id=form.f_id, od_dorm_id=dorm.d_id)
            session.add(option)
            session.commit()

    response = Response(json.dumps("Worked"), status=201, mimetype="application/json")
    return response


@app.route("/delete-form/<string:stud_id>", methods=['DELETE'])
def delete_form(stud_id):
    form = session.query(Form).filter(Form.f_student_id == stud_id).one()
    dorms = session.query(OptionD).filter(OptionD.od_form_id == form.f_id).all()
    for dorm in dorms:
        session.delete(dorm)
    roommates = session.query(OptionS).filter(OptionS.os_form_id == form.f_id).all()
    for roommate in roommates:
        session.delete(roommate)
    form = session.query(Form).filter(Form.f_id == form.f_id).one()
    session.delete(form)
    session.commit()
    response = Response(json.dumps("Worked"), status=204, mimetype="application/json")
    return response


@app.route("/modify/<int:stud_id>", methods=['PUT'])
def modify_options(stud_id):
    form = session.query(Form).filter(Form.f_student_id == stud_id).one()
    data = request.get_json()
    dorms = session.query(OptionD).filter(OptionD.od_form_id == form.f_id).all()
    for dorm in dorms:
        session.delete(dorm)
        session.commit()
    roommates = session.query(OptionS).filter(OptionS.os_form_id == form.f_id).all()
    for roommate in roommates:
        session.delete(roommate)
        session.commit()
    if data["Roommates"]:
        for s_id in data["Roommates"]:
            option = OptionS(os_form_id=form.f_id, os_student_id=s_id)
            session.add(option)
            session.commit()

    if data["Dorms"]:
        for d_id in data["Dorms"]:
            option = OptionD(od_form_id=form.f_id, od_dorm_id=d_id)
            session.add(option)
            session.commit()

    response = Response(json.dumps("Worked!"), status=200, mimetype="application.json")
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()
