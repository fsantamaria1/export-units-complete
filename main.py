"""
This script will to run daily and create a CSV from data from the MS SQL database.
"""
from os.path import dirname, join
from dotenv import load_dotenv


def main():
    """
    Main function to run the script.
    """

    # Load environment variables
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)


if __name__ == "__main__":
    main()
