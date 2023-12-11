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

@router.get("/all", response_model=list)
async def get_users(db: Session = Depends(get_db),
                    token: str = Depends(JWTBearer())):
    new_user = await user_service.get_all(db)
    access_token, refresh_token = create_all_tokens(new_user,
                                                    db,
                                                    verification=True)
    return {
        "success": True,
        "user_id": new_user.id,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.get("/{userId}", response_model=dict)
async def get_user(userId: int,
                   db: Session = Depends(get_db),
                   token=Depends(JWTBearer())):
    return await user_service.get_user(db, userId, get_data_from_token(token))

@router.post("/sign_up")
async def create_user(payload: UserCreate,
                db: Session = Depends(get_db),
                token: str = Depends(JWTBearer())):
    return await user_service.create_user(db, payload)


@router.delete("/{userId}")
async def delete_user(userId: int,
                      db: Session = Depends(get_db),
                      token: str = Depends(JWTBearer())):
    user_id = await user_service.delete_user(db, userId, get_data_from_token(token))
    return {"success": True, "user_id": user_id}
