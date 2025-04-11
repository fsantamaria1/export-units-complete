"""
This script will to run daily and create a CSV from data from the MS SQL database.
"""
import os
from os.path import dirname, join
from dotenv import load_dotenv
from resources.db_functions import run_stored_procedure


def main():
    """
    Main function to run the script.
    """

    # Load environment variables
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    run_stored_procedure(os.environ.get('schema_name'), os.environ.get('stored_procedure_name'))


if __name__ == "__main__":
    main()
