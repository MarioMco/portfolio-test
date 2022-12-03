from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Employee(BaseModel):
    parent_id: int = None
    first_name: str
    last_name: str
    middle_name: str = None
    email: EmailStr
    title: str
    hire_date: date
    gender: str


class EmployeeCreate(Employee):
    pass


class EmployeeOut(Employee):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ProductOut(BaseModel):
    id: int
    productlabel: str
    productname: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class OfferListBase(BaseModel):
    offer_id: int
    product_name: str
    price: float
    customer: str
    qty: int


class OfferListCreate(OfferListBase):
    pass


class OfferListOut(OfferListBase):
    id: int
    owner_id: int
    amount: float
    created_at = datetime
    owner: UserOut

    class Config:
        orm_mode = True
