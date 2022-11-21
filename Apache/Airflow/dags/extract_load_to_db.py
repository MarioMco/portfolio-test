from datetime import datetime
from airflow.models.dag import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.hooks.base_hook import BaseHook
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from includes.db_etl import functions as fn


DAG_CONFIG = Variable.get("sqlserver_to_postgres_etl_dag", deserialize_json=True)
SQL_PRODUCT_TABLES = DAG_CONFIG["sql_query"]["sql_product_tables"]
SQL_SALES_TABLES = DAG_CONFIG["sql_query"]["sql_sales_tables"]
EXC_API = DAG_CONFIG["exchange_rates"]["exc_api"]
EXC_APP_ID = DAG_CONFIG["exchange_rates"]["exc_app_id"]
CSV_TO_DB_PATH = DAG_CONFIG["csv_to_db"]["path"]
conn = BaseHook.get_connection("postgres")
CSV_TO_DB_HOST = conn.host
CSV_TO_DB_USER = conn.login
CSV_TO_DB_PASS = conn.password
CSV_TO_DB_DB = conn.schema
SFTP_SERVER_UPLOAD_PATH = DAG_CONFIG["sftp_server"]["upload_path"]
SFTP_SERVER_DOWNLOAD_PATH = DAG_CONFIG["sftp_server"]["download_path"]


with DAG(
    dag_id="extract_load_to_db",
    schedule_interval="0 3 * * *",
    start_date=datetime(2022, 10, 8),
    catchup=False,
    tags=["extract_load_to_db"],
) as dag:

    start_task = DummyOperator(task_id="start_task")

    with TaskGroup(
        "extract_and_load_to_psql",
        tooltip="Extract data from SQL Server or load to Postgres",
    ) as extract_sql_server_load_postgres:
        ext_product_sql_load_psql = fn.from_sql_to_postgres(SQL_PRODUCT_TABLES)
        ext_sales_sql_load_psql = fn.from_sql_to_postgres(SQL_SALES_TABLES)

        ext_product_sql_load_psql >> ext_sales_sql_load_psql

    with TaskGroup(
        "api_to_psql", tooltip="Fetch data from API and load to Postgres"
    ) as api_to_psql:
        ext_latest_exch_rate_load_psql = fn.latest_exchange_rate(EXC_API, EXC_APP_ID)

        ext_latest_exch_rate_load_psql

    with TaskGroup(
        "csv_load_to_psql", tooltip="Load data from CSV to Postgres"
    ) as csv_to_postgres:

        truncate_sql_table = PostgresOperator(
            task_id="truncate_currency_table",
            postgres_conn_id="postgres",
            sql="TRUNCATE TABLE dim_currency;",
        )

        csv_to_db = BashOperator(
            task_id="csv_to_db",
            bash_command=(
                f'psql -h {CSV_TO_DB_HOST} -d {CSV_TO_DB_DB} -U {CSV_TO_DB_USER} -w {CSV_TO_DB_PASS} -c "'
                "COPY dim_currency(currency,curreny_label,currency_name,curency_description,etl_load_id,load_date,update_date) "
                f"FROM '{CSV_TO_DB_PATH}' "
                "DELIMITER ',' "
                'CSV HEADER;"'
            ),
        )
        truncate_sql_table >> csv_to_db

    with TaskGroup(
        "sftp_load_extract", tooltip="Load from and to SFTP Server"
    ) as sftp_load_extract:

        sftp_put_file = SFTPOperator(
            task_id="sftp_put_file",
            ssh_conn_id="sftpserver",
            remote_filepath="/data/dim_channel_upload.csv",
            local_filepath=f"{SFTP_SERVER_UPLOAD_PATH}",
            operation="put",
            create_intermediate_dirs=True,
        )

        sftp_get_file = SFTPOperator(
            task_id="sftp_get_file",
            ssh_conn_id="sftpserver",
            remote_filepath="/data/dim_channel_download.csv",
            local_filepath=f"{SFTP_SERVER_DOWNLOAD_PATH}",
            operation="get",
            create_intermediate_dirs=True,
        )

        sftp_put_file >> sftp_get_file

    end_task = PythonOperator(
        task_id="end_task",
        python_callable=fn.print_task_type,
        op_kwargs={"task_type": "end"},
    )

    [
        start_task
        >> extract_sql_server_load_postgres
        >> api_to_psql
        >> csv_to_postgres
        >> sftp_load_extract
        >> end_task
    ]
