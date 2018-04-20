from datetime import datetime

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"
    personid = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(String, unique=True)
    first_name = Column(String)
    first_name_2nd = Column(String)
    surname = Column(String)
    surname_2nd = Column(String)
    orgunit = Column(String)
    cause_of_death = Column(String)
    cause_code = Column(String)
    icd10 = Column(String)
    age = Column(String)
    sex = Column(String)
    birth_date = Column(String)
    death_date = Column(String)
    interview_date = Column(String)
    national_id = Column(String)
    algorithm_version = Column(String)
    questionnaire_version = Column(String)
    created = Column(DateTime, default=datetime.now)


class Failure(Base):
    __tablename__ = "failure"
    failureid = Column(Integer, primary_key=True, autoincrement=True)
    failuretype = Column(Integer)
    failuredescription = Column(String)
    created = Column(DateTime, default=datetime.now)


class PersonFailure(Base):
    __tablename__ = "person_failure"
    personid = Column(Integer, ForeignKey(Person.personid), primary_key=True)
    failureid = Column(Integer, ForeignKey(Failure.failureid), primary_key=True)
    created = Column(DateTime, default=datetime.now)

