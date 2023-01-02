 ## [API - FastAPI](/API/FastAPI)
In this example we have used python and FastAPI Web Framework and have created multiple GET, POST, PUT and DELETE APIs. To achive this we have used libraries like:

 + sqlalchemy
   + We have used sqlalchemy to create connection with database and to create tables as well.
 + alembic
   + As sqlalchemy has a limitiation and creates tables in database but does not do any updates we are using alembic. This way we can do any updates and return to any version if needed.
 + pydantic
   + To validate data and get friendly error we have used pydantic.
 + pytest
   + We have used pytest to test our APIs and with GitHub workflows we will test it everytime new code has been pushed to GitHub.

Here is the list of all created APIs:
<img src="FastAPI docs.png" alt="FastAPI docs" title="FastAPI docs">
