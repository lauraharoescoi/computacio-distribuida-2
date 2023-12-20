from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from security import get_data_from_token
import services.Home as home_service
from schemas.Home import RegisterHome, ModifyHome

from utils.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/home",
    tags=["Home"],
)

@router.post("/")
async def register_home(payload: RegisterHome,
                        db: Session = Depends(get_db)):
    return await home_service.register_home(db, payload)
    

@router.put("/{homeId}")
async def modify_home(homeId: int,
                      payload: ModifyHome,
                      db: Session = Depends(get_db),
                      token: str = Depends(JWTBearer())):
    return await home_service.modify_home(db, homeId, payload, get_data_from_token(token))

@router.delete("/{homeId}")
async def delete_home(homeId: int,
                      db: Session = Depends(get_db),
                      token: str = Depends(JWTBearer())):
    return await home_service.delete_home(db, homeId, get_data_from_token(token))

@router.get("/{homeId}")
async def get_home_by_id(homeId: int,
                         db: Session = Depends(get_db)):
    return await home_service.get_home_by_id(db, homeId)

@router.get("/")
async def get_all_homes(db: Session = Depends(get_db)):
    return await home_service.get_all_homes(db)

@router.get("/search/{search}")
async def search_home(search: str,
                      db: Session = Depends(get_db)):
    return await home_service.search_home(db, search)

@router.get("/user/{userId}") 
async def get_homes_by_user(userId: int,
                            db: Session = Depends(get_db)):
    return await home_service.get_homes_by_user(db, userId)

@router.get("/map/{homeId}")
async def get_home_map(homeId: int,
                       db: Session = Depends(get_db)):
    return await home_service.get_home_map(db, homeId)

@router.get("/all/map")
async def get_all_homes_map(db: Session = Depends(get_db)):
    return await home_service.get_all_homes_map(db)

@router.get("/all/map/{userId}")
async def get_homes_map_by_user(userId: int,
                                db: Session = Depends(get_db)):
    return await home_service.get_homes_map_by_user(db, userId)