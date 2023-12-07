from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from security import get_data_from_token
import services.home as home_service
from schemas.home import RegisterHome, ModifyHome, DeleteHome, GetHomeById, SearchHome

from utils.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/home",
    tags=["Home"],
)

@router.post("/register", response_model=dict)
async def register_home(payload: RegisterHome,
                        db: Session = Depends(get_db),
                        token: str = Depends(JWTBearer())):
    return await home_service.register_home(db, payload, get_data_from_token(token))
    

@router.post("/modify", response_model=dict)
async def modify_home(payload: ModifyHome,
                      db: Session = Depends(get_db),
                      token: str = Depends(JWTBearer())):
    return await home_service.modify_home(db, payload, get_data_from_token(token))

@router.post("/delete/{homeId}", response_model=dict)
async def delete_home(homeId: int,
                      db: Session = Depends(get_db),
                      token: str = Depends(JWTBearer())):
    return await home_service.delete_home(db, payload, get_data_from_token(token))

@router.post("/{homeId}", response_model=dict)
async def get_home_by_id(homeId: int,
                         db: Session = Depends(get_db),
                         token: str = Depends(JWTBearer())):
    return await home_service.get_home_by_id(db, homeId)

@router.post("/search", response_model=dict)
async def search_home(payload: SearchHome,
                      db: Session = Depends(get_db),
                      token: str = Depends(JWTBearer())):
    return await home_service.search_home(db, payload)

    
