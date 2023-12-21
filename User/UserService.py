from sqlalchemy.orm import Session
from security import get_password_hash

from User.UserModel import User as ModelUser
from Token.TokenModel import TokenData

from User.UserSchema import User

from utils.service_utils import set_existing_data
from utils.service_utils import check_user
from error.AuthenticationException import AuthenticationException
from error.NotFoundException import NotFoundException


async def get_all(db: Session):
    return db.query(ModelUser).all()


async def get_user(db: Session, userId: int):
    user = db.query(ModelUser).filter(ModelUser.id == userId).first()
    if user is None:
        raise NotFoundException("User not found")
    return user


async def create_user(db: Session, user: User):
    await check_user(db, user.username)
    db_user = ModelUser(username=user.username,
                        password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, userId: int, token: TokenData):
    if not token.is_admin:
        if not (token.user_id == userId):
            raise AuthenticationException("This user does't own this user")
    try:
        deleted_rows = db.query(ModelUser).filter(ModelUser.id == userId).delete()
        db.commit()
        return deleted_rows
    except Exception as e:
        db.rollback()  # Rollback changes if an exception occurs
        print(f"Error deleting user: {e}")
        raise

async def modify_user(db: Session, userId: int, user: User):
    db_user = db.query(ModelUser).filter(ModelUser.id == userId).first()
    if db_user is None:
        raise NotFoundException("User not found")
    updated = set_existing_data(db_user, user)
    db.commit()
    db.refresh(db_user)
    return db_user


