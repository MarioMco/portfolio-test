from airflow.decorators import task
from airflow.hooks.base_hook import BaseHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from sqlalchemy import create_engine
import requests
import time
import pandas as pd


@task
def latest_exchange_rate(url: str, app_id: str):
    try:
        r = requests.get(url, params={"app_id": app_id}, timeout=30)
        r.raise_for_status()
        currency = []
        rate = []
        for k, v in r.json()["rates"].items():
            currency.append(k)
            rate.append(v)
        df = pd.DataFrame.from_dict({"currency": currency, "rate": rate})
        df["base"] = r.json()["base"]
        df["timestamp"] = r.json()["timestamp"]

        conn = BaseHook.get_connection("postgres")
        engine = create_engine(
            f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        )
        df.to_sql("exchange_rate", engine, if_exists="replace", index=False)
    except requests.exceptions.RequestException as e:
        print("API request error:")
        raise e
    except Exception as e:
        print("Exchange Rate API data processing error:")
        raise e


@task
def from_sql_to_postgres(sql_tables: list):
    try:
        start_time = time.time()
        conn = BaseHook.get_connection("postgres")
        engine = create_engine(
            f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        )
        for sql_tq in sql_tables:
            sql_table = sql_tq["table"]
            sql_query = sql_tq["query"]
            hook = MsSqlHook(mssql_conn_id="sqlserver")
            df = hook.get_pandas_df(sql_query)
            print(f"Importing {len(df)} rows into Postgresql  {sql_table} table.")

            psql_table = sql_table.lower()
            df.columns = df.columns.str.lower()
            df.to_sql(psql_table, engine, if_exists="replace", index=False)
            print(
                f"Load data for {sql_table} has finished. {str(round(time.time() - start_time, 2))} total seconds elapsed."
            )
    except Exception as e:
        print("SQL Server to Postgres data extract load error:")
        raise e


@task
def sales_by_store():
    try:
        conn = BaseHook.get_connection("postgres")
        engine = create_engine(
            f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        )
        hook = MsSqlHook(mssql_conn_id="sqlserver")
        df_store = hook.get_pandas_df("SELECT * from DimStore;")
        df_store.rename(
            columns={"StoreKey": "storekey", "StoreName": "storename"}, inplace=True
        )
        df_sales = pd.read_sql_query(
            "SELECT saleskey, storekey, salesamount from factsales;", engine
        )

        merged = df_store.merge(df_sales, on="storekey")
        store_sales = (
            merged.groupby(["storekey", "storename"])["salesamount"].sum().reset_index()
        )
        store_sales.to_sql("store_sales", engine, if_exists="replace", index=False)
    except Exception as e:
        print("Sales by Store data processing error:")
        raise e


@task
def active_stores_type_number():
    try:
        conn = BaseHook.get_connection("postgres")
        engine = create_engine(
            f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        )
        hook = MsSqlHook(mssql_conn_id="sqlserver")
        df_store_type_num = hook.get_pandas_df(
            "SELECT StoreType AS store_type, COUNT(*) AS store_num FROM DimStore WHERE Status = 'On' GROUP BY StoreType;"
        )

        df_store_type_num.to_sql(
            "active_stores_type_number", engine, if_exists="replace", index=False
        )
    except Exception as e:
        print("Sales by Store data processing error:")
        raise e


def print_task_type(**kwargs):
    """Dummy function to call before and after dependent DAG."""
    print(f"The {kwargs['task_type']} task has completed!")
