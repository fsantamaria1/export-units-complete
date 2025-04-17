"""
This script will to run daily and create a CSV from data from the MS SQL database.
"""
import os
import logging
from os.path import dirname, join
from dotenv import load_dotenv
import pandas as pd
from resources.db_functions import (
    run_stored_procedure,
    fetch_latest_units_export,
    fetch_units_by_date
)
from resources.database import Database


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_database():
    """
    Initialize the database and create the tables.
    """
    db = Database()
    db.create_tables()
    logging.info("Database initialized and tables created")


def main():
    """
    Main function to run the script.
    """
    try:

        # Load environment variables
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        # Initialize the database
        initialize_database()

        affected_rows = run_stored_procedure(os.environ.get('schema_name'), os.environ.get('stored_procedure_name'))
        logging.info("Stored procedure executed successfully")
        logging.info("Number of affected rows: %d", affected_rows)

    except Exception as e:
        logging.error("An error occurred: %s", e)
        raise e


if __name__ == "__main__":
    main()
