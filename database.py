from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import Configuration

DB_URL = Configuration.get("POSTGRESQL", "DB_URL")

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    '''returns the connetion to database'''
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.close()
    finally:
        db.close()

def db_get():
    return SessionLocal()
