from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import Home
from routers import User
from routers import Room

from error import error_handler as eh
from error.AuthenticationException import AuthenticationException
from error.NotFoundException import NotFoundException
from error.ValidationException import ValidationException
from error.InvalidDataException import InvalidDataException
from error.InputException import InputException


tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Home",
        "description": "Operations with homes.",
    },
    {
        "name": "Room",
        "description": "Operations with rooms.",
    }
]

app = FastAPI(
    title="Home Finder API",
    description="This is the API for the Home Finder App",
    version="0.0.1",
    openapi_tags=tags_metadata,
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_exception_handler(AuthenticationException,
                          eh.authentication_exception_handler)
app.add_exception_handler(NotFoundException, eh.not_found_exception_handler)
app.add_exception_handler(ValidationException, eh.validation_exception_handler)
app.add_exception_handler(InvalidDataException,
                          eh.invalid_data_exception_handler)
app.add_exception_handler(InputException, eh.input_exception_handler)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(Home.router)
app.include_router(User.router)
app.include_router(Room.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")