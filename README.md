# MS SQL Database Export Script

This project is a Python-based script designed to interact with an MS SQL database. It executes a stored procedure, fetches data, and exports the results to a CSV file. The script is intended to run daily and automate the data export process.

## Features

- Executes a stored procedure in an MS SQL database.
- Fetches the latest data from the `UnitsCompleteExport` table.
- Filters data by date and exports it to a CSV file.
- Supports environment-based configuration for database credentials and paths.
- Includes unit tests for database interactions and utility functions.

## Requirements

- Python 3.8 or higher
- MS SQL Server
- ODBC Driver 17 for SQL Server

### Python Dependencies

The required Python packages are listed in the `requirements.txt` file:

```plaintext
SQLAlchemy==2.0.40
pyodbc==5.1.0
python-dotenv==1.1.0
pandas==2.2.3
```

### Installation

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

### Setup

1. Clone the repository:
    ```bash
        git clone <repository-url>
        cd <repository-directory>
    ```
2. Configure the .env file with your database credentials and settings. Use the .env.example file as a template:  
    ```plaintext
    sql_server = 'your_server'
    sql_username = 'your_username'
    sql_password = 'your_password'
    sql_database = 'your_database'

    schema_name = 'your_schema'
    stored_procedure_name = 'your_stored_procedure'
    csv_folder_path = './csv_files/'
    ```
3. Ensure the MS SQL Server is accessible and the required stored procedure exists.  
4. Run the script:
    ```bash
    python main.py
   ```

### Usage

##### The script performs the following steps:  
 - Initializes the database and creates tables if they do not exist.
 - Executes the stored procedure specified in the .env file.
 - Fetches the latest data from the UnitsCompleteExport table.
 - Exports the data to a CSV file in the specified folder.

### Example Output
The CSV file will be saved in the csv_folder_path directory with a filename like:
```plaintext
units_complete_YYYY-MM-DD-HH-MM-SS.csv
```

### Testing
Unit tests are provided to ensure the functionality of the database interactions and utility functions. To run the tests, use pytest:

```bash
pytest tests/unit
```

### Building the UI
To create an executable for the user interface, run the following command:

```bash
python .build_ui.py
```
This will generate a .exe file in the ./dist directory. The UI allows users to run the script manually without needing to use the command line.

Project Structure
```plaintext
.
├── main.py                  # Main script to execute the workflow
├── resources/
│   ├── config.py            # Configuration for database connection
│   ├── database.py          # Database session and engine management
│   ├── db_functions.py      # Functions to interact with the database
│   ├── models.py            # SQLAlchemy models for database tables
├── tests/
│   ├── unit/
│       ├── db_functions_test.py  # Unit tests for db_functions
│       ├── database_test.py      # Unit tests for database module
│       ├── models_test.py        # Unit tests for models
│   ├── integration/
│       ├── database_test.py        # Integration tests for database interactions
│       ├── db_functions_test.py      # Integration tests for db_functions
│       ├── models_test.py          # Integration tests for models
├── .env                     # Environment variables (not included in version control)
├── .env.example             # Example environment variables file
├── requirements.txt         # Python dependencies
├── ui.py                    # User interface to run the script manually
├── .build_ui.py             # Create .exe file for the UI
└── README.md                # Project documentation
```