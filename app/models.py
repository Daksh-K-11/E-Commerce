from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Customer(Base):
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(BigInteger, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, server_default='customer')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=('now()'))