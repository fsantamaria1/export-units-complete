"""
This module contains unit tests for the database functions.
"""
from unittest.mock import MagicMock, patch
import datetime
import pytest
from resources.db_functions import run_stored_procedure
from resources.db_functions import fetch_latest_units_export, fetch_units_by_date
from resources.models import UnitsCompleteExport


class TestDbFunctionsUnit:
    """
    Class to contain the unit tests for the database functions.
    """

    @patch("resources.database.Config")
    @patch("resources.database.Database._create_engine")
    def test_call_stored_procedure_with_valid_inputs(self, _mock_create_engine, _mock_config):
        """
            Test that run_stored_procedure calls the procedure and commits the session.
        """
        schema = "ValidSchema"
        procedure_name = "ValidProcedure"

        mock_session = MagicMock()
        mock_context = MagicMock()
        mock_context.__enter__.return_value = mock_session
        mock_context.__exit__.return_value = None

        # Also patch get_new_session, so it doesn't attempt to bind anything real
        with patch("resources.database.Database.get_new_session", return_value=mock_context):
            run_stored_procedure(schema, procedure_name)

        # Assert the procedure was executed
        actual_sql = mock_session.execute.call_args[0][0].text
        expected_sql = f"EXEC [{schema}].[{procedure_name}]"
        assert actual_sql == expected_sql

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

    @patch("resources.database.Database.get_new_session")
    def test_fetch_latest_units_export_returns_latest(self, mock_get_session):
        """
        Test that fetch_latest_units_export returns the latest UnitsCompleteExport record.
        """

        mock_session = MagicMock()
        mock_instance = UnitsCompleteExport(date_created="2024-01-01 12:00:00")
        mock_session.query().order_by().first.return_value = mock_instance

        mock_context = MagicMock()
        mock_context.__enter__.return_value = mock_session
        mock_get_session.return_value = mock_context

        result = fetch_latest_units_export()
        assert result == mock_instance

    @patch("resources.database.Database.get_new_session")
    def test_fetch_units_by_date_filters_correctly(self, mock_get_session):
        """
        Test that fetch_units_by_date filters the UnitsCompleteExport records by date.
        """

        input_date = datetime.datetime(2024, 1, 1, 12, 0, 0, 123456)
        mock_session = MagicMock()
        expected_results = [UnitsCompleteExport(), UnitsCompleteExport()]
        mock_session.query().filter().all.return_value = expected_results

        mock_context = MagicMock()
        mock_context.__enter__.return_value = mock_session
        mock_get_session.return_value = mock_context

        result = fetch_units_by_date(input_date)
        assert result == expected_results
