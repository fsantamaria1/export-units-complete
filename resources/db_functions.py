"""
Contains functions to interact with the database.
"""
from sqlalchemy import text
from resources.database import Database


def run_stored_procedure(schema, procedure_name):
    """
    Calls the specified stored procedure using the current database engine.

    :param schema: The name of the schema where the procedure is stored
    :param procedure_name: The name of the stored procedure to call
    """
    # Validate schema and procedure_name
    if not schema or not procedure_name:
        raise ValueError("Schema and procedure name must be provided.")
    if not schema.isidentifier() or not procedure_name.isidentifier():
        raise ValueError("Invalid schema or procedure name")

    db = Database()
    with db.get_new_session() as session:
        session.execute(text(f"EXEC {schema}.{procedure_name}"))
        session.commit()
