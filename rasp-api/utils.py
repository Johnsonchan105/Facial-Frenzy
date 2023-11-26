import os, sys, dotenv, argparse, random, traceback
import dropbox
from dropbox.exceptions import AuthError, ApiError
from PIL import Image
from io import BytesIO
from datetime import datetime
from passlib.hash import sha256_crypt
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from db import db_session
from models import Players

dotenv.load_dotenv() #set the environment variables from .env file

'''
helper functions for db
'''
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"

def get_player_by_tag_from_db(gamertag):
    return db_session.query(Players).filter(Players.gamertag == gamertag).one_or_none()

def get_player_by_name_from_db(name):
    return db_session.query(Players).filter(Players.name == name).one_or_none()

def get_player_by_id_from_db(uid):
    return db_session.query(Players).filter(Players.user_id == uid).one_or_none()

def add_player_to_db(name, gamertag):
    obj = None
    try:
        obj = get_player_from_db(gamertag)
        if not obj:
            obj= Players(
                name=name,
                gamertag=gamertag
            )
            db_session.add(obj)
            db_session.commit()
        else:
            print(f"add_player_to_db: player already exists in DB with id: {obj.user_id}")
    except Exception as e:
        print("Exception in add_user_to_db: {}".format(e))
        traceback.print_exc()

def add_players_in_list_to_db(plist):
    for player in plist:
        add_player_to_db(player[0], player[1])

'''
helper functions for dropbox
'''
DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_APP_ACCESS_TOKEN")

def upload_image_to_dropbox(image_path, destination_path):
    try:
        # init dropbox cli
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

        with open(image_path, 'rb') as f:
            dbx.files_upload(f.read(), destination_path)

        print(f"Image '{image_path}' uploaded to Dropbox at '{destination_path}'")

    except AuthError as e:
        print(f"Error: {e}")
    except ApiError as e:
        print(f"API Error: {e}")

def download_image_from_dropbox(source_path):
    try:
        # init dropbox cli
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        # download img
        metadata, response = dbx.files_download(source_path)
        image_data = response.content

        # return img
        return Image.open(BytesIO(image_data))
    except AuthError as e:
        print(f"Error: {e}")
    except ApiError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")