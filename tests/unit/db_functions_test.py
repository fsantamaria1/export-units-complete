"""
This module contains unit tests for the database functions.
"""
from unittest.mock import MagicMock, patch
import pytest
from resources.db_functions import run_stored_procedure
from resources.database import Database


class TestDbFunctionsUnit:
    """
    Class to contain the unit tests for the database functions.
    """
    def test_call_stored_procedure_with_valid_inputs(self):
        """
        Test calling a stored procedure with valid schema and procedure name.
        """
        schema = "ValidSchema"
        procedure_name = "ValidProcedure"
        mock_session = MagicMock()

        with patch.object(Database, 'get_new_session', return_value=mock_session):
            run_stored_procedure(schema, procedure_name)

        # Extract the actual SQL string passed to execute
        actual_sql = mock_session.execute.call_args[0][0].text # noqa
        expected_sql = "EXEC ValidSchema.ValidProcedure"

        assert actual_sql == expected_sql
        mock_session.commit.assert_called_once()

    def test_raises_error_when_schema_is_none(self):
        """
        Test calling a stored procedure with None schema name.
        """
        with pytest.raises(ValueError, match="Schema and procedure name must be provided."):
            run_stored_procedure(None, "ValidProcedure")

    def test_raises_error_when_procedure_name_is_none(self):
        """
        Test calling a stored procedure with None procedure name.
        """
        with pytest.raises(ValueError, match="Schema and procedure name must be provided."):
            run_stored_procedure("ValidSchema", None)

    def test_raises_error_for_invalid_schema_name(self):
        """
        Test calling a stored procedure with invalid schema name.
        """
        with pytest.raises(ValueError, match="Invalid schema or procedure name"):
            run_stored_procedure("DROP TABLE user-data; --", "ValidProcedure")

    def test_raises_error_for_invalid_procedure_name(self):
        """
        Test calling a stored procedure with invalid procedure name.
        """
        with pytest.raises(ValueError, match="Invalid schema or procedure name"):
            run_stored_procedure("ValidSchema", "DROP TABLE user-data; --")
