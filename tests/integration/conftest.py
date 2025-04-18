"""
This module contains fixtures for the integration tests.
"""
import random
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from resources.config import Config
from resources.database import Database
from resources.models import UnitsCompleteExport
from tests.utils import create_units_complete_export

# Create a single engine for the entire test suite
engine = create_engine(Config().sqlalchemy_database_uri, echo=True)
# Bind the session to the engine
Session = sessionmaker(bind=engine)


def generate_unique_primary_key(model, pk_column, start=1000, end=999999):
    """Generate a random integer for the primary key and ensure it doesn't exist in the database."""
    while True:
        with Session(bind=engine) as session:
            random_pk = random.randint(start, end)  # Generate a random integer within the range
            try:
                # Try querying the database for an existing primary key
                session.query(model).filter(pk_column == random_pk).one()
            except NoResultFound:
                # If no result found, the primary key is unique
                return random_pk


@pytest.fixture(name='db_connection', scope="module")
def db_connection_fixture():
    """
    Fixture to create a database connection for the entire test module.
    """
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(name="db_session", scope="function")
def db_session_fixture(db_connection):
    """
    Fixture to create a new database session for each test function.
    """
    transaction = db_connection.begin_nested()
    session = Session(bind=db_connection)
    yield session
    session.close()

    if transaction.is_active:
        transaction.rollback()


@pytest.fixture(name='valid_units_complete_export', scope='function')
def valid_units_complete_export_fixture():
    """
    Fixture to create a valid UnitsCompleteExport object for testing.
    """
    # Generate a unique primary key for the UnitsCompleteExport object
    export_id = generate_unique_primary_key(UnitsCompleteExport, UnitsCompleteExport.export_id)
    return create_units_complete_export(export_id=export_id)


@pytest.fixture(scope="module")
def db_instance():
    """
    Fixture to create a Database instance connected to the actual database.
    """
    db = Database()
    yield db
    db.close()
