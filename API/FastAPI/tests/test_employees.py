from typing import List
from app import schemas
import pytest

def test_get_all_employees(authorized_client, test_employees):
    res = authorized_client.get('/employees')
    
    assert res.status_code == 200
    
def test_unauthorized_user_get_all_employees(client, test_employees):
    res = client.get('/employees/')
    
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_employee(client, test_employees):
    res = client.get(f'/employees/{test_employees[0].id}')
    
    assert res.status_code == 401
    
def test_get_one_employee_not_exist(authorized_client, test_employees):
    res = authorized_client.get('/employees/234532')
    
    assert res.status_code == 404
    
def test_get_one_employee(authorized_client, test_employees):
    res = authorized_client.get(f'/employees/{test_employees[0].id}')
    employee  = schemas.EmployeeOut(**res.json())
    
    assert res.status_code == 200
    assert employee.parent_id == test_employees[0].parent_id
    assert employee.id == test_employees[0].id
    assert employee.title == test_employees[0].title
    assert employee.email == test_employees[0].email
    assert employee.hire_date == test_employees[0].hire_date
    assert employee.first_name == test_employees[0].first_name
    assert employee.last_name == test_employees[0].last_name
    assert employee.middle_name == test_employees[0].middle_name
    
@pytest.mark.parametrize("parent_id, first_name, last_name, middle_name, email, title, hire_date, gender", [
    (1, "Jack", "Dong", "Nick", "jack@test.com", "CEO", "2022-10-01","M"),
    (1, "George", "James", "Tim", "george@test.com", "Manager", "2022-08-01","M"),
    (2, "Lilly", "Rider", "Karen", "lilly@test.com", "HR", "2018-02-01","F")
])
def test_create_employee(authorized_client, test_user, test_employees, parent_id, first_name, last_name, middle_name, email, title, hire_date, gender):
    employee_data = {"parent_id": parent_id, "first_name": first_name, "last_name": last_name, "middle_name": middle_name, "email": email, "title": title, "hire_date": hire_date, "gender": gender}
    res = authorized_client.post("/employees/", json = employee_data)
    created_employee = schemas.Employee(**res.json())
    print(hire_date)
    
    assert res.status_code == 201
    assert created_employee.parent_id == parent_id
    assert created_employee.first_name == first_name
    assert created_employee.last_name == last_name
    assert created_employee.middle_name == middle_name
    assert created_employee.email == email
    assert created_employee.title == title
    assert str(created_employee.hire_date) == hire_date
    assert created_employee.gender == gender
    
def test_unauthorized_user_delete_employee(client, test_user, test_employees):
    res = client.delete(f"/employees/{test_employees[0].id}")
    assert res.status_code == 401
    
def test_delete_employee_success(authorized_client, test_user, test_employees):
    res = authorized_client.delete(f"/employees/{test_employees[0].id}")
    assert res.status_code == 204
    
def test_delete_employee_non_exist(authorized_client, test_user, test_employees):
    res = authorized_client.delete("/employees/423508734")
    assert res.status_code == 404
    
def test_unauthorized_user_update_employee(client, test_user, test_employees):
    res = client.put(f"/employees/{test_employees[0].id}")
    assert res.status_code == 401
    
def test_update_employee_non_exist(authorized_client, test_user, test_employees):
    data = {"parent_id": 3, 
            "first_name": "Jamie", 
            "last_name": "Timbo", 
            "middle_name": "Hugh", 
            "email": "jamie@test.com", 
            "title": "CEO", 
            "hire_date": "2022-01-01", 
            "gender": "M"}
    res = authorized_client.put(f"/employees/{test_employees[0].id}", json=data)
    upadated_employee = schemas.EmployeeCreate(**res.json())
    
    assert res.status_code == 200
    assert upadated_employee.parent_id == data["parent_id"]
    assert upadated_employee.first_name == data["first_name"]
    assert upadated_employee.last_name == data["last_name"]
    assert upadated_employee.middle_name == data["middle_name"]
    assert upadated_employee.email == data["email"]
    assert upadated_employee.title == data["title"]
    assert str(upadated_employee.hire_date) == data["hire_date"]
    assert upadated_employee.gender == data["gender"]
    
