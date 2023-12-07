from models.Home import Home
from models.User import User

from database import SessionLocal, engine

from schemas.home import RegisterHome, ModifyHome, DeleteHome, GetHomeById, SearchHome


def register_home(db: SessionLocal, home: RegisterHome, user: User):
    db_home = Home(name=home.name, address=home.address, description=home.description, owner=user.id, location=home.location)
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    return db_home

def modify_home(db: SessionLocal, home: ModifyHome, user: User):
    db_home = db.query(Home).filter(Home.id == home.id).first()
    if db_home.owner == user.id:
        db_home.name = home.name
        db_home.address = home.address
        db_home.description = home.description
        db.commit()
        db.refresh(db_home)
        return db_home
    else:
        return None

def delete_home(db: SessionLocal, home: DeleteHome, user: User):
    db_home = db.query(Home).filter(Home.id == home.id).first()
    if db_home.owner == user.id:
        db.delete(db_home)
        db.commit()
        return True
    else:
        return False

def get_home_by_id(db: SessionLocal, home: GetHomeById):
    db_home = db.query(Home).filter(Home.id == home.id).first()
    return db_home

def search_home(db: SessionLocal, search: SearchHome):
    db_home = db.query(Home).filter(Home.address.like("%" + search.text + "%") | Home.description.like("%" + search.text + "%")).all()
    return db_home


def list_homes_info(db: SessionLocal, home: GetHomeById):
    if home.id == 0:
        db_homes = db.query(Home).all()
        return db_homes
    else:
        db_home = db.query(Home).filter(Home.id == home.id).first()
        return db_home

