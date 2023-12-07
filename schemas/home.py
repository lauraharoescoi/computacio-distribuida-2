from pydantic import BaseModel, constr, conlist, validator
from typing import List

class Home(BaseModel):
    id: int
    name: constr(min_length=1, max_length=50)
    address: constr(min_length=1, max_length=100)
    description: constr(min_length=1, max_length=500)
    owner: int
    location: List[float]


class RegisterHome(BaseModel):
    name: constr(min_length=1, max_length=50)
    address: constr(min_length=1, max_length=100)
    description: constr(min_length=1, max_length=500)
    location: List[float]

class ModifyHome(BaseModel):
    id: int
    name: constr(min_length=1, max_length=50)
    address: constr(min_length=1, max_length=100)
    description: constr(min_length=1, max_length=500)

class DeleteHome(BaseModel):
    id: int

class GetHomeById(BaseModel):
    id: int

class SearchHome(BaseModel):
    text: constr(min_length=1, max_length=100)

