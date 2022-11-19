import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv


# DB connection
try:
    load_dotenv()
    SQLUID = os.getenv("SQLUID")
    SQLPASSWORD = os.getenv("SQLPASSWORD")
    DRIVER = "ODBC Driver 18 for SQL Server"
    SQLSERVER = "localhost"
    SQLDB = "ContosoRetailDW"
    engine_stmt = f"mssql+pyodbc://{SQLUID}:{SQLPASSWORD}@{SQLSERVER}/{SQLDB}?TrustServerCertificate=yes&driver={DRIVER}"
    engine = create_engine(engine_stmt)
    engine.connect()
    print("DB connection established.")
except SQLAlchemyError as e:
    print("Error: DB connection failed!", e.__cause__, sep="\n")
    sys.exit()
    


def fetch_all_sql_data(table_name: str) -> pd.DataFrame:
    """Function will return all data from database for a given table.

    Args:
        table_name (str): SQL Table name.

    Returns:
        pd.DataFrame: All data from database for a given table as pandas DataFrame.
    """
    try:
        sql = f"SELECT * FROM {table_name}"
        data = pd.read_sql(sql, engine)
        return data
    except Exception as e:
        print(f"{table_name} fetch all data has failed: {e}")
        sys.exit()
    finally:
        print(f"Fetch all data from {table_name} has finished.")


def fetch_sql_data(sql_query: str) -> pd.DataFrame:
    """Function will return a DataFrame containing data from the database for a given query.

    Args:
        sql_query (str): SQL Query.

    Returns:
        pd.DataFrame: All data from the database for the given query.
    """
    try:
        data = pd.read_sql(sql_query, engine)
        return data
    except Exception as e:
        print(f'Fetch data for SQL query: "{sql_query}" has failed: {e}')
        sys.exit()
    finally:
        print(f'Fetch data for SQL Query: "{sql_query}" has finished.')