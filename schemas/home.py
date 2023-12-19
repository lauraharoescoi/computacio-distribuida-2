from pydantic import BaseModel, constr, conlist, validator
from typing import List, Optional

class Home(BaseModel):
    name: constr(min_length=1, max_length=50)
    address: constr(min_length=1, max_length=100)
    description: constr(min_length=1, max_length=500)
    owner: int
    location: str


class RegisterHome(BaseModel):
    name: constr(min_length=1, max_length=50)
    address: constr(min_length=1, max_length=100)
    description: constr(min_length=1, max_length=500)
    owner: int
    location: str


class ModifyHome(BaseModel):
    name: Optional[constr(min_length=1, max_length=50)]
    address: Optional[constr(min_length=1, max_length=100)]
    description: Optional[constr(min_length=1, max_length=500)]
    owner: Optional[int]
