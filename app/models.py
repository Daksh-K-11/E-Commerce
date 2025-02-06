from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Text, Numeric
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
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
    
    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    store_name = Column(String, nullable=False)
    business_license = Column(String, nullable=False, unique=True)
    tax_id = Column(String, nullable=False, unique=True)

    user = relationship("User", back_populates="seller", uselist=False, cascade="all, delete")


User.seller = relationship("Seller", back_populates="user", uselist=False)


Seller.products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    extra_specifications = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=('now()'))
    
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    seller = relationship("Seller", back_populates="products")


class ProductImage(Base):
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String, nullable=False)
    
    product = relationship("Product", back_populates="images")