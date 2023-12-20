from Home.HomeModel import Home as ModelHome
from models.TokenData import TokenData

from utils.service_utils import check_home

from utils.service_utils import set_existing_data
from error.NotFoundException import NotFoundException
from error.AuthenticationException import AuthenticationException
from shapely import from_wkb

from fastapi.responses import HTMLResponse
import os
import pandas as pd 
import plotly.express as px

from database import SessionLocal

from Home.HomeSchema import RegisterHome, ModifyHome
from geoalchemy2 import WKTElement
from sqlalchemy import func


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
    
    
async def get_homes_nearby_map(db: SessionLocal, latitude: float, longitude: float, radius: float):
    point = WKTElement(f'POINT({longitude} {latitude})', srid=4326)

    db_homes = db.query(ModelHome).filter(
        func.ST_DWithin(ModelHome.location, point, radius)
    ).all()

    if not db_homes:
        raise ValueError("No se encontraron casas cercanas")

    data = [{
        'Name': home.name,
        'Address': home.address,
        'Description': home.description,
        'Owner': home.owner,
        'Lat': float(str(from_wkb(str(home.location))).split(" ")[1].replace("(", "")),
        'Long': float(str(from_wkb(str(home.location))).split(" ")[2].replace(")", ""))
    } for home in db_homes]

    df = pd.DataFrame(data)
    file_path = "./static/map_nearby_homes.html"
    await generate_map(df, latitude, longitude, file_path, 'red', 'green')
    with open(file_path, "rb") as f:
        img = f.read()
    return HTMLResponse(content=img, media_type="text/html")



async def generate_map(df, center_lat, center_lon, file_path, marker_color="blue", center_marker_color="green"):
    try:
        fig = px.scatter_mapbox(
            df, 
            hover_name="Name", 
            hover_data=["Address", "Description", "Owner"],
            lat="Lat", 
            lon="Long", 
            color_discrete_sequence=[marker_color]
        )

        # Añadir un marcador para el punto central
        fig.add_trace(px.scatter_mapbox(
            pd.DataFrame([{'Name': 'Punto Central', 'Lat': center_lat, 'Long': center_lon}]),
            hover_name="Name", 
            color_discrete_sequence=[center_marker_color],
            lat="Lat", 
            lon="Long", 
            
        ).data[0])

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        fig.write_html(file_path)
    except Exception as e:
        print(f"Error al generar el mapa: {e}")
        raise e


