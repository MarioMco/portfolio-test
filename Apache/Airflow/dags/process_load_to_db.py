from datetime import datetime
from airflow.models.dag import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.utils.task_group import TaskGroup
from includes.db_etl import functions as fn


with DAG(
    dag_id="process_load_to_db",
    schedule_interval="0 3 * * *",
    start_date=datetime(2022, 10, 8),
    catchup=False,
    tags=["process_load_to_db"],
) as dag:

    extract_load_to_db_sensor = ExternalTaskSensor(
        task_id="extract_load_to_db_sensor",
        external_dag_id="extract_load_to_db",
        retries=2,
    )

    with TaskGroup(
        "data_processing_load", tooltip="Process data and load to Postgres"
    ) as data_processing_load:
        sales_by_store = fn.sales_by_store()
        active_stores_type_number = fn.active_stores_type_number()

        [sales_by_store, active_stores_type_number]

    extract_load_to_db_sensor >> data_processing_load
