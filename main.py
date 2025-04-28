"""
This script will run daily and create a CSV from data from the MS SQL database.
"""
import os
import logging
import pandas as pd
from resources.db_functions import (
    run_stored_procedure,
    fetch_latest_units_export,
    fetch_units_by_date
)
from resources.database import initialize_database


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def filter_and_export_data(df, filter_col, value, base_file_name, csv_folder_path):
    """
    Filter the DataFrame based on the given column and value, and export to CSV.

    :param df: The DataFrame to filter
    :param filter_col: The column to filter on
    :param value: The value to filter by
    :param base_file_name: The base file name for the CSV file
    :param csv_folder_path: The folder path to save the CSV file
    """
    filtered_df = df[df[filter_col] == value].drop(
        columns=['missing_from_budget', 'in_closed_period']
    )
    file_name = f'{base_file_name}_{filter_col}_{value}.csv'
    file_path = os.path.join(csv_folder_path, file_name)
    filtered_df.to_csv(file_path, index=False)
    logging.info("CSV file created successfully: %s", file_path)
    logging.info("Number of records for %s %s: %d", filter_col, value, len(filtered_df))


def main():
    """
    Main function to run the script.
    """
    try:

        # Initialize the database
        initialize_database()

        # Create CSV folder if it doesn't exist
        csv_folder_path = os.environ.get('csv_folder_path')
        if not csv_folder_path:
            logging.error("CSV folder path is not set in environment variables.")
            raise ValueError("Missing CSV folder path")
        if not os.path.exists(csv_folder_path):
            os.makedirs(csv_folder_path)
            logging.info("CSV folder created: %s", csv_folder_path)

        affected_rows = run_stored_procedure()
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

            # Convert units_completed to a list of dictionaries
            units_completed_data = [unit.to_dict() for unit in units_completed]

            # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(units_completed_data)

            base_file_name = f'UC_{latest_date.strftime("%Y%m%d%H%M%S")}'

            # Filter and export data for missing_from_budget = 1
            filter_and_export_data(df, 'missing_from_budget', 1, base_file_name, csv_folder_path)
            # Filter and export data for in_closed_period = 1
            filter_and_export_data(df, 'in_closed_period', 1, base_file_name, csv_folder_path)

            # Dataframe for records not in closed period
            not_in_closed_period_df = df[df['in_closed_period'] != 1].drop(
                columns=['missing_from_budget', 'in_closed_period'])

            # Create a separate CSV file for each job_date
            for job_date, group in not_in_closed_period_df.groupby('job_date'):
                try:
                    safe_job_date = pd.to_datetime(job_date).strftime("%Y%m%d")
                    file_name = f'UC_{latest_date.strftime("%Y%m%d%H%M%S")}_{safe_job_date}.csv'
                    csv_file_path = os.path.join(csv_folder_path, file_name)

                    group.to_csv(csv_file_path, index=False)

                    logging.info("CSV file created successfully: %s", csv_file_path)
                    logging.info("Number of records for job_date %s: %d", job_date, len(group))
                except Exception as e:
                    logging.error("Failed to create CSV for job_date %s: %s", job_date, e)
                    raise e

            logging.info("Total number of records: %d", len(units_completed_data))
            return affected_rows
        logging.warning("No rows were affected by the stored procedure execution.")
        logging.info("No data to process.")
        return 0

    except Exception as e:
        logging.error("An error occurred: %s", e)
        raise e


if __name__ == "__main__":
    main()
