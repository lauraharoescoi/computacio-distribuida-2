from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from security import get_data_from_token
from schemas.Room import RegisterRoom, ModifyRoom
import services.Room as room_service

from utils.auth_bearer import JWTBearer


router = APIRouter(
    prefix="/room",
    tags=["room"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register")
async def register(room: RegisterRoom, 
                   db: Session = Depends(get_db)):
    return await room_service.register_room(db, room)

@router.put("/{roomId}")
async def modify(roomId: int, 
                 room: ModifyRoom, 
                 db: Session = Depends(get_db)):
    return await room_service.modify_room(db, roomId, room)

@router.delete("/{roomId}")
async def delete(roomId: int, 
                 db: Session = Depends(get_db)):
    return await room_service.delete_room(db, roomId)

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

