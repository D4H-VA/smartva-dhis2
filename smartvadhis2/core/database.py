import os

from logzero import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from .exceptions.base import (
    SmartVADHIS2Exception,
    DbException
)

from .exceptions import db_exceptions
from .config import DatabaseConfig
from .models import Person, Failure, PersonFailure
from .mapping import Mapping


class Database(object):
    """Local database"""
    def __init__(self, db_url=None):
        self.db_queries_log = DatabaseConfig.db_queries_log
        if not db_url:
            self.db_filename = os.path.join(DatabaseConfig.database_dir, DatabaseConfig.db_name)
            self.db_url = r'sqlite:///{}'.format(self.db_filename)
        else:
            self.db_filename = db_url.replace('sqlite:///', '')
            self.db_url = db_url

        if not os.path.exists(self.db_filename):
            self._create_db()
            self._insert_failure_categories()
        else:
            logger.info("Using database: {}".format(self.db_filename))
        # create database
        self.engine = create_engine(self.db_url, echo=self.db_queries_log)

    def _create_db(self):
        """Insert SQLAlchemy model (create tables). Removes the file if it fails"""
        try:
            engine = create_engine(self.db_url, echo=self.db_queries_log)
            logger.info("Creating database schema...")
            Person.__table__.create(bind=engine)
            Failure.__table__.create(bind=engine)
            PersonFailure.__table__.create(bind=engine)

        except (OSError, SQLAlchemyError):
            os.remove(self.db_filename)
            raise DbException("Could not create database at '{}".format(self.db_filename))
        except Exception as e:
            os.remove(self.db_filename)
            logger.exception("Unknown exception occurred: %s", e)
            import sys
            sys.exit(1)

    def _insert_failure_categories(self):
        """Insert Exception categories into `failure` sourced from core.exceptions.__init__"""
        logger.info("Adding exceptions to database...")
        logger.info("Parsing exception to insert into database...")
        all_exceptions = db_exceptions
        engine = create_engine(self.db_url, echo=self.db_queries_log)
        Session = sessionmaker(bind=engine)
        session = Session()
        failure_types = [
            {
                "failureid": err.code,
                "failuretype": err.err_type,
                "failuredescription": err.message
            }
            for err in all_exceptions
        ]

        try:
            f = [Failure(**failure) for failure in failure_types]
            session.add_all(f)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            os.remove(self.db_filename)
            raise SmartVADHIS2Exception(e)
        except Exception as e:
            session.rollback()
            os.remove(self.db_filename)
            logger.exception("Unknown exception occurred: %s", e)
        finally:
            session.close()

    def write_errors(self, data, errors):
        """Entry method to write any errors sourced from the application"""
        if not isinstance(errors, list):
            # we need a list to iterate even if it's just one item
            errors = [errors]
        values = self._to_sql_rows(data)

        Session = sessionmaker(bind=self.engine)
        session = Session()

        personid = self._write_person(session, values)

        for err in errors:
            f = PersonFailure(personid=personid, failureid=err.code)
            failure = session.query(PersonFailure)\
                .filter(PersonFailure.personid == f.personid,
                        PersonFailure.failureid == f.failureid)\
                .one_or_none()
            if not failure:
                try:
                    session.add(f)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    session.close()
                    raise SmartVADHIS2Exception(e)
        session.close()

    @staticmethod
    def _write_person(session, values):
        """Write a Person instance to the database
        but re-use the record if it's already existing
        and return the personid
        """
        p = Person(**values)
        person = session.query(Person).filter(Person.sid == p.sid).one_or_none()
        if not person:
            person = p
            try:
                session.add(person)
                session.flush()
            except Exception as e:
                session.rollback()
                raise SmartVADHIS2Exception(e)
        return person.personid

    @staticmethod
    def _to_sql_rows(data):
        """Convert data rows to a dict ready for insertion"""
        try:
            d = {
                mapping.code_name: data[mapping.csv_name]
                for mapping in Mapping.properties()
                if mapping.csv_name is not None
            }
        except KeyError as e:
            raise SmartVADHIS2Exception("Mapping is not aligned with CSV rows %s", e)
        else:
            return d

    def query(self, query):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session.query(query)


# "singleton" for db connection
database = Database()


def get_db():
    return database
