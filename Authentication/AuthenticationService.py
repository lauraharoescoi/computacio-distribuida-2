from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from User.UserModel import User as ModelUser


from security import create_all_tokens, get_data_from_token, verify_password

from error.InvalidDataException import InvalidDataException
from error.AuthenticationException import AuthenticationException

async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(ModelUser).filter(ModelUser.username == username).first()
    if user is None:
        raise InvalidDataException("User not found")
    if not verify_password(password, user.password):
        raise AuthenticationException("Incorrect password")
    access_token, refresh_token = create_all_tokens(user, db)
    return {
        "user_id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }


async def reset_password(username: str, db: Session = Depends(get_db)):
    user = db.query(ModelUser).filter(ModelUser.username == username).first()
    if user is None:
        raise InvalidDataException("User not found")
    if not user.is_verified:
        raise InvalidDataException("User not verified")
    create_all_tokens(user, db, True)
    return {"success": True}


async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    data = get_data_from_token(refresh_token, True)
    if data is None:
        raise InvalidDataException("Invalid token")
    user = db.query(ModelUser).filter(ModelUser.id == data.user_id).first()
    if user is None:
        raise InvalidDataException("User not found")
    if not (refresh_token == user.refresh_token):
        raise InvalidDataException("Invalid token")
    return create_all_tokens(user, db)