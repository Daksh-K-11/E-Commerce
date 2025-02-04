# from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
# from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.orm import relationship
# from .database import Base

# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     phone_number = Column(BigInteger, nullable=False, unique=True)
#     email = Column(String, nullable=False, unique=True)
#     address = Column(String, nullable=True)
#     password = Column(String, nullable=False)
#     role = Column(String, nullable=False, server_default='user')
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=('now()'))
    
    
# class Seller(Base):
#     __tablename__ = 'sellers'
    
#     id = Column(Integer, ForeignKey("users.id", on_delete="CASCADE"), nullable=False, primary_key=True)
#     user = relationship("User")
#     store_name = Column(String, nullable=False)
#     business_license = Column(String, nullable=False, unique=True)
#     tax_id = Column(String, nullable=False, unique=True)

from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
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


class Seller(Base):
    __tablename__ = 'sellers'
    
    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)  # ✅ Corrected primary key
    store_name = Column(String, nullable=False)
    business_license = Column(String, nullable=False, unique=True)
    tax_id = Column(String, nullable=False, unique=True)

    user = relationship("User", back_populates="seller", uselist=False, cascade="all, delete")


User.seller = relationship("Seller", back_populates="user", uselist=False)
