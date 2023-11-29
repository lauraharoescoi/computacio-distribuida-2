from datetime import date
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from database import Base
from sqlalchemy.orm import deferred

from sqlalchemy.orm import Mapped

class User(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    password = Mapped[str] = deferred(Column(String))
    token = Mapped[str] = deferred(Column(String, default=""))
