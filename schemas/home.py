from pydantic import BaseModel, constr, conlist, validator, Field
from typing import List, Optional
from geoalchemy2.types import WKBElement
from typing_extensions import Annotated

class Home(BaseModel):
    name: constr(min_length=1, max_length=50)
    address: constr(min_length=1, max_length=100)
    description: constr(min_length=1, max_length=500)
    owner: int
    location: Annotated[str, WKBElement] = Field('POINT (3 5)')


class RegisterHome(BaseModel):
    name: constr(min_length=1, max_length=50)
    address: constr(min_length=1, max_length=100)
    description: constr(min_length=1, max_length=500)
    owner: int
    location: Annotated[str, WKBElement] = Field('POINT (3 5)')


class ModifyHome(BaseModel):
    name: Optional[constr(min_length=1, max_length=50)]
    address: Optional[constr(min_length=1, max_length=100)]
    description: Optional[constr(min_length=1, max_length=500)]
    owner: Optional[int]
