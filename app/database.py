from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

from .config import settings

database_password = urllib.parse.quote_plus(settings.database_password)

postgres_url = f'postgresql://{settings.database_username}:{database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
print(postgres_url)

engine = create_engine(postgres_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        