from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from security import get_data_from_token
from Room.RoomSchema import Room, ModifyRoom
import Room.RoomService as room_service

from utils.auth_bearer import JWTBearer


router = APIRouter(
    prefix="/room",
    tags=["Room"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register")
async def register(room: Room, 
                   db: Session = Depends(get_db)):
    return await room_service.register_room(db, room)

@router.put("/{roomId}")
async def modify(roomId: int, 
                 room: ModifyRoom, 
                 db: Session = Depends(get_db),
                 data: dict = Depends(JWTBearer())):
    return await room_service.modify_room(db, roomId, room, get_data_from_token(data))

@router.delete("/{roomId}")
async def delete(roomId: int, 
                 db: Session = Depends(get_db),
                 data: dict = Depends(JWTBearer())):
    return await room_service.delete_room(db, roomId, get_data_from_token(data))

@router.get("/{roomId}")
async def get_by_id(roomId: int, 
                    db: Session = Depends(get_db)):
    return await room_service.get_room_by_id(db, roomId)

@router.get("/search/{search}")
async def search(search: str, 
                 db: Session = Depends(get_db)):
    return await room_service.search_room(db, search)

@router.get("/")
async def get_all_rooms(db: Session = Depends(get_db)):
    return await room_service.get_all_rooms(db)

@router.get("/home/{homeId}")
async def get_by_home(homeId: int, 
                      db: Session = Depends(get_db)):
    return await room_service.get_room_by_home(db, homeId)

