from fastapi import Depends, APIRouter
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from security import get_data_from_token, sec
from database import get_db
from services import Authentication as auth_service
from utils.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/login")
async def login(credentials: HTTPBasicCredentials = Depends(sec),
                db: Session = Depends(get_db)):
    username = credentials.username
    password = credentials.password
    return await auth_service.login(username, password, db)


@router.post("/reset-password")
async def reset_password(username: str, db: Session = Depends(get_db)):
    return await auth_service.reset_password(username, db)


@router.post("/refresh-token")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    return await auth_service.refresh_token(refresh_token, db)


@router.get("/me")
async def get_me(token: str = Depends(JWTBearer())):
    return get_data_from_token(token)