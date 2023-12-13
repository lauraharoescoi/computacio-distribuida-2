from models.Home import Home as ModelHome
from models.User import User as ModelUser
from models.Room import Room as ModelRoom

from utils.service_utils import set_existing_data
from error.NotFoundException import NotFoundException

from database import SessionLocal, engine

from schemas.Room import RegisterRoom, ModifyRoom, SearchRoom

async def register_room(db: SessionLocal, room: RegisterRoom):
    db_room = ModelRoom(name=room.name, home=room.home, sensor=room.sensor)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

async def modify_room(db: SessionLocal, roomId: int, room: ModifyRoom):
    db_room = db.query(ModelRoom).filter(ModelRoom.id == roomId).first()
    if db_room is None:
        raise NotFoundException("Room not found")
    updated = set_existing_data(db_room, room)
    db.commit()
    db.refresh(db_room)
    return db_room

async def delete_room(db: SessionLocal, roomId: int):
    db_room = db.query(ModelRoom).filter(ModelRoom.id == roomId).first()
    db.delete(db_room)
    db.commit()
    return db_room

async def get_room_by_id(db: SessionLocal, roomId: int):
    db_room = db.query(ModelRoom).filter(ModelRoom.id == roomId).first()
    return db_room

async def search_room(db: SessionLocal, search: str):
    db_room = db.query(ModelRoom).filter(ModelRoom.name.like("%" + search + "%")).all()
    return db_room

async def get_all_rooms(db: SessionLocal):
    db_rooms = db.query(ModelRoom).all()
    return db_rooms

async def get_room_by_home(db: SessionLocal, homeId: int):
    db_rooms = db.query(ModelRoom).filter(ModelRoom.home == homeId).all()
    return db_rooms
 