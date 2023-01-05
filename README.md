# Data Engineering - ETL, Apache Airflow and Kafka, FastAPI, SQL, Data Analysis and Data Visualization

### Built with

+ Apache 
  + Airflow
  + Kafka

+ API
  + FastAPI
    +  sqlalchemy
    +  pydantic
    +  alembic 
    + pytest

+ Python
  + Pandas
  + matplotlib
  + seaborn
  + psycopg2
  + requests
  + sqlalchemy
  + dotenv
  + Tools:
    + VSCode
    + Jupyter Notebook

+ SQL
	+ SQL Server
	+ PostgreSQL
  + Tools:
	  + Azure Data Studio
	  + Dbeaver

+ Cloud
  + Azure
    + Azure Functions 
  + AWS
    + Lambda
    + API Gateway

+ Power BI
  + DAX
  + M
  
+ CI/CD
  + GitHub Actions


## [SQL](/BD)
Here we have used Docker to run SQL Server on Mac and ContosoRetailDW as database. We have created [ER Diagram](/DB/ER%20Diagram/) with draw.io, and written [SQL Query](/DB/SQL%20Query/) with CTE, JOINS, Triggers, Procedures, Variables etc., and have [analyzed data with Python](/DB/Analytics/Python/): 
+ [SQL Query](/DB/SQL%20Query/)
+ [ER Diagram](/DB/ER%20Diagram/)
+ [Docker - SQL Server on Mac](/DB/Docker/)
+ [data analysis and data visualization](/DB/Analytics/Python/) with Python.

## [Data Visualization with Power BI](/PowerBI)
In this example we have used data from ContosoRetailDW database were we have created multiple [DAX queries](/PowerBI/DAX.txt) and [Dashboard](PowerBI/Dashboard.png). To get data we have connected directly to SQL Server.
<img src="PowerBI/Dashboard.png" alt="Contosodb Dashboard" title="Contosodb Dashboard">

## [Python Data Analysis](/DB/Analytics/Python/)
In this example we have showed how to connect to SQL Server with [Python, analyze and visualize data](DB/Analytics/Python/). Here is the list of libraires we have used:
 + pandas
 + numpy
 + seaborn
 + matplotlib
 + sqlalchemy
 + dotenv

## [Apache Airflow](/Apache/Airflow)
In this example we have created data pipeline with Apache Airflow. We have used different Airflow operators and sensors to extract, transform and load data. We have extract data from SQL Server, API, SFTP Server and store it in Postgres DB. Here is the list of Hooks, Operators and Sensors we have used:
 + PythonOperator
 + BashOperator
 + SFTPOperator
 + PostgresOperator
 + DummyOperator
 + ExternalTaskSensor
 + BaseHook
 + MsSqlHook
 
 ### ETL
 <img src="Apache/Airflow/etl_to_db.png" alt="ETL to DB" title="ETL to DB">
 
 ### External Task Sensor and Processing
 <img src="Apache/Airflow/etl_processing.png" width="300" alt="ETL and Processing" title="ETL and Processing">
 
 ## [API - FastAPI](/API/FastAPI) and [Azure Function - FastAPI](/API/Azure-FastAPI)
 In this example we have used python and FastAPI Web Framework and have created multiple GET, POST, PUT and DELETE APIs. To achive this we have used libraries like:
 + sqlalchemy
 + pydantic
 + alembic
 + pytest
 
 We have used Azure Function and published API with [Azure](/API/Azure-FastAPI)
 
  <img src="/API/FastAPI/FastAPI docs.png" alt="FastAPI docs" title="FastAPI docs">
  
 ## [CI/CD - GitHub Actions](/.github/workflows)
 Here we are using GitHub Actions to test our FastAPI code everytime after we push or pull new code to or from GitHub.
 
 
