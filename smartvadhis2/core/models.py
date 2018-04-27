from datetime import datetime

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
Module for SQLALchemy model declaration (used by local database)
"""


class Person(Base):
    """Person Model"""
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
    created = Column(DateTime, default=datetime.now)


class Failure(Base):
    """Failure model, storing Exception categories, e.g. Import Errors, Validation Errors"""
    __tablename__ = "failure"
    failureid = Column(Integer, primary_key=True)
    failuretype = Column(Integer)
    failuredescription = Column(String)
    created = Column(DateTime, default=datetime.now)


class PersonFailure(Base):
    """PersonFailure model, linking Persons to Failure"""
    __tablename__ = "person_failure"
    personid = Column(Integer, ForeignKey(Person.personid), primary_key=True)
    failureid = Column(Integer, ForeignKey(Failure.failureid), primary_key=True)
    created = Column(DateTime, default=datetime.now)

