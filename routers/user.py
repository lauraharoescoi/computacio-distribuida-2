from fastapi import Depends, Response, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from security import get_data_from_token, create_all_tokens
import services.User as user_service
from utils.auth_bearer import JWTBearer

from schemas.User import UserBase, UserCreate

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.get("/all")
async def get_users(db: Session = Depends(get_db),
                    token: str = Depends(JWTBearer())):
    new_user = await user_service.get_all(db)
    return new_user


@router.get("/{userId}")
async def get_user(userId: int,
                   db: Session = Depends(get_db)):
    return await user_service.get_user(db, userId)
    

@router.post("/sign_up")
async def create_user(payload: UserCreate,
                db: Session = Depends(get_db),
                token: str = Depends(JWTBearer())):
    return await user_service.create_user(db, payload)


@router.delete("/{userId}")
async def delete_user(userId: int,
                      db: Session = Depends(get_db)):

    return user_service.delete_user(db, userId)
