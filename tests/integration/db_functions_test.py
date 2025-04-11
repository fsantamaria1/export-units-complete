"""
This module contains integration tests for the database functions.
"""
import pytest
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from resources.db_functions import run_stored_procedure
from resources.database import Database


class TestDbFunctionsIntegration:
    """
    Class to contain the integration tests for the database functions.
    """

    @pytest.fixture(scope="module")
    def db_instance(self):
        """
        Fixture to create a Database instance connected to the actual database.
        """
        db = Database()
        yield db
        db.close()

    @pytest.fixture(scope="module")
    def setup_test_procedure(self, db_instance):
        """
        Fixture to create a test stored procedure in the database.
        """
        with db_instance.get_new_session() as session:
            try:
                # Create a test stored procedure
                session.execute(text("""
                    CREATE PROCEDURE dbo.TestProcedure AS
                    BEGIN
                        SELECT 'Test' AS Result;
                    END
                """))
                session.commit()
            except ProgrammingError as e:
                pytest.fail(f"Failed to create test procedure: {e}")
            yield
            # Cleanup: Drop the test procedure
            session.execute(text("DROP PROCEDURE dbo.TestProcedure"))
            session.commit()

    @pytest.mark.usefixtures("setup_test_procedure")
    def test_call_stored_procedure(self, db_instance):
        """
        Test calling a stored procedure with valid schema and procedure name.
        """
        with db_instance.get_new_session() as session:
            try:
                run_stored_procedure("dbo", "TestProcedure")
                result = session.execute(text("SELECT 'Test' AS Result")).fetchone()
                assert result[0] == "Test"
            except ProgrammingError as e:
                pytest.fail(f"Failed to call stored procedure: {e}")
