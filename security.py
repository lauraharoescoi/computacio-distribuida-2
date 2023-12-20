from datetime import datetime, timedelta
from dateutil import parser
from fastapi.security import OAuth2PasswordBearer, HTTPBasic
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from passlib.hash import pbkdf2_sha256

from User.UserModel import User as ModelUser
from models.TokenData import TokenData as TD
from config import Configuration

from error import AuthenticationException, NotFoundException

SECRET_KEY = Configuration.get("SECURITY", "SECRET_KEY")
ALGORITHM = Configuration.get("SECURITY", "ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = Configuration.get("SECURITY",
                                                "ACCESS_TOKEN_EXPIRE_MINUTES")

SERVICE_TOKEN = Configuration.get("SECURITY", "SERVICE_TOKEN")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
sec = HTTPBasic()


def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)
    # return True


def get_password_hash(password):
    return pbkdf2_sha256.hash(password)
    # return password


def is_service_token(token: str):
    return token == SERVICE_TOKEN


def get_user(user_id: int, db: Session):
    user = db.query(ModelUser).filter(ModelUser.id == user_id).first()
    if not user:
        raise NotFoundException("User not found")
    return user


def verify_token(token: str, db: Session):
    # token = req.headers["Authorization"]
    if is_service_token(token):
        return True
    dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = get_user(dict["user_id"], db)
    if user.token != token:
        raise AuthenticationException("Invalid token")
    # Here your code for verifying the token or whatever you use
    if parser.parse(dict["expt"]) < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")
    return True


def update_tokens(user_id: int,
                  db: Session,
                  access_token: str = None,
                  refresh_token: str = None):
    user = get_user(user_id, db)
    if access_token is not None:
        user.token = access_token
    if refresh_token is not None:
        user.refresh_token = refresh_token
    db.commit()
    db.refresh(user)


def create_access_token(user: ModelUser,
                        db: Session,
                        expires_delta: timedelta = None):
    to_encode = {
        'user_id': user.id,
        'username': user.username,
    }

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    

    
    to_encode.update({"expt": expire.isoformat()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    update_tokens(user.id, db, access_token=encoded_jwt)

    return encoded_jwt


def create_refresh_token(user: ModelUser,
                         db: Session,
                         expires_delta: timedelta = None):
    to_encode = {'user_id': user.id, 'username': user.username}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    update_tokens(user.id, db, refresh_token=encoded_jwt)
    return encoded_jwt


def get_data_from_token(token: str = Depends(oauth2_scheme),
                        refresh: bool = False,
                        special: bool = False):
    d = TD()
    if is_service_token(token):
        d.is_admin = True
        d.is_service = True
        d.user_id = 0
        d.available = True
        d.type = "service"
        d.username = ""
        return d
    data = decode_token(token)
    d.user_id = data.get("user_id")
    d.expt = data.get("expt")
    d.username = data.get("username")
    return d


def decode_token(token):
    return jwt.decode(token.encode('utf-8'),
                      SECRET_KEY,
                      algorithms=[ALGORITHM])


def create_all_tokens(user: ModelUser,
                      db: Session):
    access_token = create_access_token(user, db)
    refresh_token = create_refresh_token(user, db)
    return access_token, refresh_token