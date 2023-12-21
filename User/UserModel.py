from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import deferred

from sqlalchemy.orm import Mapped

class User(Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    password: Mapped[str] = deferred(Column(String))
    token: Mapped[str] = deferred(Column(String, default=""))
    refresh_token: Mapped[str] = deferred(Column(String, default=""))

    