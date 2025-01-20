from sqlalchemy import Column, Integer, String
from .database import Base

class Customer(Base):
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(Integer, nullable=False, unique=True)
    