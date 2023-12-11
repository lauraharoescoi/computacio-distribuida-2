from sqlalchemy.orm import Session
from security import get_password_hash

from models.User import User as ModelUser
from models.TokenData import TokenData

from schemas.User import UserBase, UserCreate

from utils.service_utils import check_image
from error.AuthenticationException import AuthenticationException
from error.NotFoundException import NotFoundException

from utils.hide_utils import user_show_private


async def get_all(db: Session):
    return db.query(ModelUser).all()


async def get_user(db: Session, userId: int, data: TokenData):
    user = db.query(ModelUser).filter(ModelUser.id == userId).first()
    if user is None:
        raise NotFoundException("User not found")
    return user


async def create_user(db: Session, user: UserCreate):
    db_user = ModelUser(username=user.username,
                        password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def delete_user(db: Session, userId: int):
    try:
        deleted_rows = await db.query(ModelUser).filter(ModelUser.id == userId).delete()
        db.commit()
        return deleted_rows
    except Exception as e:
        db.rollback()  # Rollback changes if an exception occurs
        print(f"Error deleting user: {e}")
        raise

