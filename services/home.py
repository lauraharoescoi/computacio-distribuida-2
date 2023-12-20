from models.Home import Home as ModelHome
from models.User import User
from models.TokenData import TokenData

from utils.service_utils import check_home

from utils.service_utils import set_existing_data
from error.NotFoundException import NotFoundException
from error.AuthenticationException import AuthenticationException
from shapely import from_wkb

from fastapi.responses import Response

import pandas as pd 
import plotly.express as px

from database import SessionLocal, engine

from schemas.Home import RegisterHome, ModifyHome


async def register_home(db: SessionLocal, home: RegisterHome):
    await check_home(db, home.address)
    db_home = ModelHome(name=home.name, address=home.address, description=home.description, owner=home.owner, location=home.location)
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    db_home.location = str(from_wkb(str(db_home.location)))
    return db_home

async def modify_home(db: SessionLocal, homeId: int, home: ModifyHome, data: TokenData):
    if not data.is_admin:
        if not (data.user_id == homeId):
            raise AuthenticationException("This user does't own this home")
    db_home = db.query(ModelHome).filter(ModelHome.id == homeId).first()
    if db_home is None:
        raise NotFoundException("Home not found")
    updated = set_existing_data(db_home, home)
    db.commit()
    db.refresh(db_home)
    db_home.location = str(from_wkb(str(db_home.location)))
    return db_home

async def delete_home(db: SessionLocal, homeId: int, data: TokenData):
    if not data.is_admin:
        if not (data.user_id == homeId):
            raise AuthenticationException("This user does't own this home")
    db_home = db.query(ModelHome).filter(ModelHome.id == homeId).first()
    db.delete(db_home)
    db.commit()
    db_home.location = str(from_wkb(str(db_home.location)))
    return db_home

async def get_home_by_id(db: SessionLocal, HomeId: int):
    db_home = db.query(ModelHome).filter(ModelHome.id == HomeId).first()
    db_home.location = str(from_wkb(str(db_home.location)))
    return db_home

async def search_home(db: SessionLocal, search: str):
    db_home = db.query(ModelHome).filter(ModelHome.address.like("%" + search + "%") | ModelHome.description.like("%" + search + "%")).all()
    for home in db_home:
        home.location = str(from_wkb(str(home.location)))
    return db_home

async def get_all_homes(db: SessionLocal):
    db_homes = db.query(ModelHome).all()
    for home in db_homes:
        home.location = str(from_wkb(str(home.location)))
    return db_homes


async def list_homes_info(db: SessionLocal, home: int):
    if home.id == 0:
        db_homes = db.query(ModelHome).all()
        return db_homes
    else:
        db_home = db.query(ModelHome).filter(ModelHome.id == home.id).first()
        return db_home

async def get_homes_by_user(db: SessionLocal, user: int):
    db_home = db.query(ModelHome).filter(ModelHome.owner == user).all()
    for home in db_home:
        home.location = str(from_wkb(str(home.location)))
    return db_home

async def get_home_map(db: SessionLocal, homeId: int):
    db_home = db.query(ModelHome).filter(ModelHome.id == homeId).first()
    db_home.location = str(from_wkb(str(db_home.location)))
    lat = db_home.location.split(" ")[1].replace("(", "")
    long = db_home.location.split(" ")[2].replace(")", "")
    df = pd.DataFrame({'Lat': [int(lat)], 'Long': [int(long)]})
    fig = px.scatter_mapbox(df, lat="Lat", lon="Long", zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.write_image("/static/map.png") 
    # fig.write_html("static/map.html")
    with open("static/map.png", "r", encoding='utf8') as f:
        img = f.read()
    return Response(img, media_type="image/png")