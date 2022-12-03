from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, nullable=False)
    parent_id = Column(Integer, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    hire_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class OfferList(Base):
    __tablename__ = "offers_list"

    id = Column(Integer, primary_key=True, nullable=False)
    offer_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Float(precision=10, decimal_return_scale=2), nullable=False)
    qty = Column(Integer, nullable=False)
    amount = Column(Float(precision=10, decimal_return_scale=2), nullable=False)
    customer = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")
