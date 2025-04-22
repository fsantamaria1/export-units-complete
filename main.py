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

        affected_rows = run_stored_procedure(
            os.environ.get('schema_name'),
            os.environ.get('stored_procedure_name')
        )
        logging.info("Stored procedure executed successfully")
        logging.info("Number of affected rows: %d", affected_rows)

        # Run rest of the script if affected_rows > 0
        if affected_rows > 0:

            # Get the latest units complete export
            latest_record = fetch_latest_units_export()

            if not latest_record:
                logging.warning("No UnitsCompleteExport records found.")
                return 0

            latest_date = latest_record.date_created
            logging.info("Latest units complete record date: %s", latest_date)

            units_completed = fetch_units_by_date(latest_date)

            logging.info("Units completed data fetched successfully")

            # Create CSV file
            csv_folder_path = os.environ.get('csv_folder_path')
            if not csv_folder_path:
                logging.error("CSV folder path is not set in environment variables.")
                raise ValueError("Missing CSV folder path")
            if not os.path.exists(csv_folder_path):
                os.makedirs(csv_folder_path)
            csv_file_path = os.path.join(
                csv_folder_path,
                f'units_complete_{latest_date.strftime("%Y-%m-%d-%H-%M-%S")}.csv'
            )

            # Convert units_completed to a list of dictionaries
            units_completed_data = [unit.to_dict() for unit in units_completed]

            # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(units_completed_data)

            # Save the DataFrame to a CSV file
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                df.to_csv(csvfile, index=False)

            logging.info("CSV file created successfully: %s", csv_file_path)
            logging.info("number of records: %d", len(units_completed_data))
            return affected_rows
        logging.warning("No rows were affected by the stored procedure execution.")
        logging.info("No data to process.")
        return 0

    except Exception as e:
        logging.error("An error occurred: %s", e)
        raise e


if __name__ == "__main__":
    main()
