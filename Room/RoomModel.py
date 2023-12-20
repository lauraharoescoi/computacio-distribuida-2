from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Room(Base):
    __tablename__ = "room"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=False, index=True)
    home: int = Column(Integer, ForeignKey("home.id", ondelete="CASCADE"))
    sensor: str = Column(String, unique=False, index=True)