# conftest is a special file that pytest uses and it allows to define fictures

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import models
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    
@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "test213"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@gmail.com", "password": "test123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_employees(test_user, session):
    employee_data = [
        {"parent_id": 1, "first_name": "Joe", "last_name": "Doe", "middle_name": "Nick", "email": "joe@test.com","title": "Manager", "hire_date": "2022-10-01","gender": "M"},
        {"parent_id": 1, "first_name": "Tim", "last_name": "Logan", "middle_name": None, "email": "tim@test.com","title": "Data Engineer", "hire_date": "2020-01-01","gender": "M"},
        {"parent_id": 1, "first_name": "Anna", "last_name": "Lopez", "middle_name": "Jane", "email": "anna@test.com","title": "HR", "hire_date": "2018-01-10","gender": "F"}
    ]
    
    def create_employee_model(employee):
        return models.Employee(**employee)
    
    employee_map = map(create_employee_model, employee_data)
    employees_list = list(employee_map)
    session.add_all(employees_list)
    session.commit()
    employees = session.query(models.Employee).all()
    return employees