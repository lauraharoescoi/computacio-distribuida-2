from models.Home import Home as ModelHome
from models.User import User

from utils.service_utils import set_existing_data
from error.NotFoundException import NotFoundException

from database import SessionLocal, engine

from schemas.Home import RegisterHome, ModifyHome, DeleteHome, GetHomeById, SearchHome


async def register_home(db: SessionLocal, home: RegisterHome):
    db_home = ModelHome(name=home.name, address=home.address, description=home.description, owner=home.owner, location=home.location)
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    return db_home

async def modify_home(db: SessionLocal, homeId: int, home: ModifyHome):
    db_home = db.query(ModelHome).filter(ModelHome.id == homeId).first()
    if db_home is None:
        raise NotFoundException("Home not found")
    updated = set_existing_data(db_home, home)
    db.commit()
    db.refresh(db_home)
    return db_home

async def delete_home(db: SessionLocal, homeId: int):
    db_home = db.query(ModelHome).filter(ModelHome.id == homeId).first()
    db.delete(db_home)
    db.commit()
    return db_home

async def get_home_by_id(db: SessionLocal, HomeId: GetHomeById):
    db_home = db.query(ModelHome).filter(ModelHome.id == HomeId).first()
    return db_home

async def search_home(db: SessionLocal, search: str):
    db_home = db.query(ModelHome).filter(ModelHome.address.like("%" + search + "%") | ModelHome.description.like("%" + search + "%")).all()
    return db_home

async def get_all_homes(db: SessionLocal):
    db_homes = db.query(ModelHome).all()
    return db_homes


async def list_homes_info(db: SessionLocal, home: GetHomeById):
    if home.id == 0:
        db_homes = db.query(ModelHome).all()
        return db_homes
    else:
        db_home = db.query(ModelHome).filter(ModelHome.id == home.id).first()
        return db_home

