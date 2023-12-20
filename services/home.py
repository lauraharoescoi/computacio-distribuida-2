from models.Home import Home as ModelHome
from models.User import User
from models.TokenData import TokenData

from utils.service_utils import check_home

from utils.service_utils import set_existing_data
from error.NotFoundException import NotFoundException
from error.AuthenticationException import AuthenticationException
from shapely import from_wkb

from fastapi.responses import Response, HTMLResponse
import os
import pandas as pd 
import plotly.express as px

from database import SessionLocal, engine

from schemas.Home import RegisterHome, ModifyHome
from geoalchemy2 import WKTElement





async def register_home(db: SessionLocal, home: RegisterHome):
    await check_home(db, home.address)
    lat, lon = home.location
    location_wkt = WKTElement(f'POINT({lon} {lat})')
    db_home = ModelHome(name=home.name, address=home.address, description=home.description, owner=home.owner, location=location_wkt)
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    db_home.location = str(from_wkb(str(db_home.location)))
    return db_home

async def modify_home(db: SessionLocal, homeId: int, home: ModifyHome, data: TokenData):
    db_home = db.query(ModelHome).filter(ModelHome.id == homeId).first()
    if db_home is None:
        raise NotFoundException("Home not found")
    if not data.is_admin:
        if not (data.user_id == db_home.owner):
            raise AuthenticationException("This user does't own this home")
    updated = set_existing_data(db_home, home)
    db.commit()
    db.refresh(db_home)
    db_home.location = str(from_wkb(str(db_home.location)))
    return db_home

async def delete_home(db: SessionLocal, homeId: int, data: TokenData):
    db_home = db.query(ModelHome).filter(ModelHome.id == homeId).first()
    if db_home is None:
        raise NotFoundException("Home not found")
    if not data.is_admin:
        if not (data.user_id == db_home.owner):
            raise AuthenticationException("This user does't own this home")
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
    try:
        # Obtener datos de la base de datos
        db_home = db.query(ModelHome).filter(ModelHome.id == homeId).first()
        if not db_home:
            raise ValueError(f"No se encontró la casa con ID {homeId}")

        db_home.location = str(from_wkb(str(db_home.location)))
        lat = db_home.location.split(" ")[1].replace("(", "")
        long = db_home.location.split(" ")[2].replace(")", "")
        df = pd.DataFrame({'Lat': [float(lat)], 'Long': [float(long)]})

        # Ruta del archivo
        file_path = "./static/map_all.html"
        
        await generate_map(df, file_path)
    except Exception as e:
        # Error al generar el mapa
        print(f"Error al generar el mapa: {e}")

    try:
        # Leer y devolver la imagen
        with open(file_path, "rb") as f:
            img = f.read()
        return HTMLResponse(content=img, media_type="text/html")
    except Exception as e:
        # Error al leer el archivo
        print(f"Error al leer el archivo: {e}")


async def get_all_homes_map(db: SessionLocal):
    try:
        # Obtener datos de varias casas de la base de datos
        db_homes = db.query(ModelHome).all()  # O ajusta esta consulta según tus necesidades
        if not db_homes:
            raise ValueError("No se encontraron casas")

        # Preparar los datos para Plotly
        data = []
        for home in db_homes:
            location = str(from_wkb(str(home.location)))
            lat = location.split(" ")[1].replace("(", "")
            long = location.split(" ")[2].replace(")", "")
            data.append({'Lat': float(lat), 'Long': float(long)})

        df = pd.DataFrame(data)
        file_path = "./static/map_all.html"
        await generate_map(df, file_path)
    except Exception as e:
        print(f"Error al generar el mapa: {e}")

    try:
        with open(file_path, "rb") as f:
            img = f.read()
        return HTMLResponse(content=img, media_type="text/html")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        

async def get_homes_map_by_user(db: SessionLocal, user: int):
    try:
        # Obtener datos de varias casas de la base de datos
        db_homes = db.query(ModelHome).filter(ModelHome.owner == user).all()  # O ajusta esta consulta según tus necesidades
        if not db_homes:
            raise ValueError("No se encontraron casas")

        # Preparar los datos para Plotly
        data = []
        for home in db_homes:
            location = str(from_wkb(str(home.location)))
            lat = location.split(" ")[1].replace("(", "")
            long = location.split(" ")[2].replace(")", "")
            data.append({'Lat': float(lat), 'Long': float(long)})

        df = pd.DataFrame(data)
        file_path = "./static/map_by_user.html"
        await generate_map(df, file_path)
    except Exception as e:
        print(f"Error al generar el mapa: {e}")

    try:
        with open(file_path, "rb") as f:
            img = f.read()
        return HTMLResponse(content=img, media_type="text/html")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
    
       
async def generate_map(df, file_path):
    try:
        fig = px.scatter_mapbox(df, lat="Lat", lon="Long", zoom=10)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        fig.write_html(file_path)
    except Exception as e:
        print(f"Error al generar el mapa: {e}")
        raise e
