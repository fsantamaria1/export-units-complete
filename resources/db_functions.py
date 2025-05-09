"""
Contains functions to interact with the database.
"""
import os
from datetime import timedelta
from typing import List
from sqlalchemy import text
from resources.database import Database
from resources.models import UnitsCompleteExport


def run_stored_procedure(
        schema: str = None,
        procedure_name: str = None
) -> int:
    """
    Calls the specified stored procedure using the current database engine.

    :param schema: The name of the schema where the procedure is stored
    :param procedure_name: The name of the stored procedure to call
    :return: The number of affected rows
    :raises ValueError: If the schema or procedure name is invalid
    """
    # Get schema and procedure name from environment variables if not provided
    schema = schema or os.environ.get('schema_name')
    procedure_name = procedure_name or os.environ.get('stored_procedure_name')

    # Validate schema and procedure_name
    if not schema or not procedure_name:
        raise ValueError("Schema and procedure name must be provided.")
    if not schema.isidentifier() or not procedure_name.isidentifier():
        raise ValueError("Invalid schema or procedure name")

    db = Database()
    with db.get_new_session() as session:
        # Execute the stored procedure
        result = session.execute(text(f"EXEC [{schema}].[{procedure_name}]"))

        # Fetch only the first row
        row = result.fetchone()

        # Commit the session
        session.commit()

        if row:
            # Access the first column of the row
            affected_rows = row[0]
            return affected_rows
        # Return 0 if no rows are present
        return 0


def fetch_latest_units_export() -> UnitsCompleteExport:
    """
    Fetches the most recent UnitsCompleteExport record from the database.

    :return: The most recent UnitsCompleteExport record with truncated microseconds.
    """
    db = Database()
    with db.get_new_session() as session:
        latest_export = session.query(
            UnitsCompleteExport
        ).order_by(
            UnitsCompleteExport.date_created.desc()
        ).first()
        return latest_export


def fetch_units_by_date(date) -> List[UnitsCompleteExport]:
    """
    Fetches the UnitsCompleteExport record for a specific date.
    """
    # Truncate the input date to milliseconds
    date = date.replace(microsecond=(date.microsecond // 1000) * 1000)

    start = date - timedelta(milliseconds=2)
    end = date + timedelta(milliseconds=2)

    db = Database()
    with db.get_new_session() as session:
        units_completed = session.query(UnitsCompleteExport).filter(
            UnitsCompleteExport.date_created.between(start, end)
        ).all()
        return units_completed
