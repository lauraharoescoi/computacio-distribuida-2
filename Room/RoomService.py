from Home.HomeModel import Home as ModelHome
from Room.RoomModel import Room as ModelRoom
from models.TokenData import TokenData

from utils.service_utils import set_existing_data
from error.NotFoundException import NotFoundException
from error.AuthenticationException import AuthenticationException

from database import SessionLocal

from Room.RoomSchema import Room, ModifyRoom

async def register_room(db: SessionLocal, room: Room):
    db_home = db.query(ModelHome).filter(ModelHome.id == room.home).first()
    if db_home is None:
        raise NotFoundException("Home not found")
    db_room = ModelRoom(name=room.name, home=room.home, sensor=room.sensor)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

async def modify_room(db: SessionLocal, roomId: int, room: ModifyRoom, data: TokenData):
    db_room = db.query(ModelRoom).filter(ModelRoom.id == roomId).first()
    if db_room is None:
        raise NotFoundException("Room not found")
    db_home = db.query(ModelHome).filter(ModelHome.id == db_room.home).first()
    if db_home is None:
        raise NotFoundException("Room without a home")
    if not data.is_admin:
        if not (data.user_id == db_home.owner):
            raise AuthenticationException("This user does't own this room")
    updated = set_existing_data(db_room, room)
    db.commit()
    db.refresh(db_room)
    return db_room

async def delete_room(db: SessionLocal, roomId: int, data: TokenData):
    db_room = db.query(ModelRoom).filter(ModelRoom.id == roomId).first()
    if db_room is None:
        raise NotFoundException("Room not found")
    db_home = db.query(ModelHome).filter(ModelHome.id == db_room.home).first()
    if db_home is None:
        raise NotFoundException("Room without a home")
    if not data.is_admin:
        if not (data.user_id == db_home.owner):
            raise AuthenticationException("This user does't own this room")
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
 