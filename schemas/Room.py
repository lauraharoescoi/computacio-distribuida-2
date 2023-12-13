from pydantic import BaseModel, constr, conlist, validator
from typing import List, Optional

class Room(BaseModel):
    id: int
    name: constr(min_length=1, max_length=50)
    home: int
    sensor: str
    
class RegisterRoom(BaseModel):
    name: constr(min_length=1, max_length=50)
    home: int
    sensor: str
    
class ModifyRoom(BaseModel):
    name: Optional[constr(min_length=1, max_length=50)]
    home: Optional[int]
    sensor: Optional[str]
    
class SearchRoom(BaseModel):
    text: constr(min_length=1, max_length=100)
    
    