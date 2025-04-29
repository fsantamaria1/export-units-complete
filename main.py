"""
This script will run daily and create CSVs from data in the MS SQL database.
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


def export_dataset(df, file_name, csv_folder_path, description=""):
    """
    Exports a DataFrame to CSV with logging.

    :param df: DataFrame to export
    :param file_name: Output file name
    :param csv_folder_path: Output directory
    :param description: Optional description for logging
    """
    try:
        file_path = os.path.join(csv_folder_path, file_name)

        clean_df = df.drop(columns=['missing_from_budget'])
        clean_df.to_csv(file_path, index=False)

        log_msg = f"Created {file_path} ({len(clean_df)} records)"
        if description:
            log_msg += f" - {description}"
        logging.info(log_msg)
    except Exception as e:
        logging.error("Failed to export %s: %s", file_name, e)
        raise


def main():
    """
    Main processing workflow for generating CSV exports.
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

        # Execute the stored procedure
        affected_rows = run_stored_procedure()
        logging.info("Stored procedure executed successfully")
        logging.info("Number of affected rows: %d", affected_rows)

        if affected_rows <= 0:
            logging.info("No data changes - exiting")
            return 0

        # Get latest data
        latest_record = fetch_latest_units_export()
        if not latest_record:
            logging.warning("No UnitsCompleteExport records found")
            return 0

        latest_date = latest_record.date_created
        units_completed = fetch_units_by_date(latest_date)
        logging.info("Fetched %d completed units", len(units_completed))

        # Prepare data for export
        base_name = f'UC_{latest_date.strftime("%Y%m%d%H%M%S")}'
        df = pd.DataFrame([unit.to_dict() for unit in units_completed])

        # Export missing budget data
        missing_budget_df = df[df['missing_from_budget'] == 1]
        if not missing_budget_df.empty:
            export_dataset(
                missing_budget_df,
                f'{base_name}_missing_from_budget.csv',
                csv_folder_path,
                "Missing budget entries"
            )

        # Export data grouped by job_date
        for job_date, group_df in df.groupby('job_date'):
            try:
                safe_date = pd.to_datetime(job_date).strftime("%Y%m%d")
                export_dataset(
                    group_df,
                    f'{base_name}_{safe_date}.csv',
                    csv_folder_path,
                    f"Job date {job_date}"
                )
            except Exception as e:
                logging.error("Failed to process job date %s: %s", job_date, e)
                raise

        logging.info("Total processed records: %d", len(units_completed))
        return affected_rows

    except Exception as e:
        logging.error("An error occurred: %s", e)
        raise e


if __name__ == "__main__":
    main()
