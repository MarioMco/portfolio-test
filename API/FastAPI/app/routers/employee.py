from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi_pagination import Page, add_pagination, paginate
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=Page[schemas.EmployeeOut])
def get_employees(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    employees = db.query(models.Employee).all()
    
    return paginate(employees)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeOut
)
def create_user(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    new_employee = models.Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


@router.get("/{id}", response_model=schemas.EmployeeOut)
def get_employee(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id: {id} not found",
        )

    return employee


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    employee = db.query(models.Employee).filter(models.Employee.id == id)
    if employee.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id: {id} does not exist.",
        )

    employee.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.EmployeeOut)
def update_employee(
    id: int,
    updated_employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    employee_query = db.query(models.Employee).filter(models.Employee.id == id)
    employee = employee_query.first()
    if employee == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id: {id} does not exist.",
        )

    employee_query.update(updated_employee.dict())
    db.commit()
    return employee_query.first()

add_pagination(router)

