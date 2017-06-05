import models as db
from passlib.apps import custom_app_context as pwd_context
import getpass

def hash_password(password):
        return pwd_context.encrypt(password)

def validate_station(station_id):
        try:
            station_id = int(station_id)
            return True
        except ValueError:
            return False

def validate_username(username):
        return isinstance(username, str)

def create_user(username, password, station_id):
    hashed_password = hash_password(password)
    db.insertUser(username, hashed_password, station_id)

if __name__ == "__main__":
    username = raw_input("Username for booth: ")
    while (not validate_username(username)):
        username = raw_input("Username can only be characters, input username: ")

    password = getpass.getpass("Password: ")

    station_id = raw_input("Station id: ")
    while (not validate_station(station_id)):
        station_id = raw_input("Station id can only be integer, input station id: ")

    create_user(username, password, station_id)
