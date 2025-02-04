from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(BigInteger, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default='user')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=('now()'))
    
    
# class Seller(Base):
#     __tablename__ = 'sellers'
    
    