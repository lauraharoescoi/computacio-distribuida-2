import string
import random
import base64

from error.ValidationException import ValidationException
from User.UserModel import User
from Home.HomeModel import Home


def get_user_by_username(db, username):
    return db.query(User).filter(User.username == username).first()


def get_home_by_address(db, address):
    return db.query(Home).filter(Home.address == address).first()


async def check_user(db, username):
    if get_user_by_username(db, username) is not None:
        raise ValidationException("Username already exists")
    

async def check_home(db, name):
    if get_home_by_address(db, name) is not None:
        raise ValidationException("Home already exists")


def set_existing_data(db_obj, req_obj):
    data = req_obj.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(db_obj, key, value)
    return list(data.keys())


def generate_random_code(length):
    return ''.join(
        random.choice(string.ascii_uppercase) for _ in range(length))


def generate_complex_random_code(length):
    return ''.join(random.choice(string.printable) for _ in range(length))


def subtract_lists(list1, list2):
    return [item for item in list1 if item not in list2]
