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
from models import Players, Facial

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

def update_player_score(uid, points):
    player = get_player_by_id_from_db(uid)
    player.wins += points
    db_session.commit()
    
def add_player_to_db(name, gamertag):
    obj = None
    try:
        obj = get_player_by_tag_from_db(gamertag)
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

def add_player_image(user_id, path):
    obj = None
    try:
        obj = db_session.query(Facial).filter(Facial.img_path == path).one_or_none()
        if not obj:
            obj= Facial(
                user_id=user_id,
                img_path=path
            )
            db_session.add(obj)
            db_session.commit()
        else:
            print(f"add_player_image: image already exists in DB with id: {obj.img_path}")
    except Exception as e:
        print("Exception in add_player_image: {}".format(e))
        traceback.print_exc()

def get_player_images_paths(user_id):
    '''
    Get's top 5 images of player
    '''
    try:
        facials = db_session.query(Facial).filter(Facial.user_id == user_id).limit(5)
        facial_img_paths = [facial.img_path for facial in facials]
        return facial_img_paths
    except Exception as e:
        print("Exception in get_player_images: {}".format(e))
        traceback.print_exc()

def compress_image(image_data, quality=85):
    """
    Compress an image in a Flask FileStorage object with Pillow.

    Parameters:
    - file_storage: Flask FileStorage object representing the input image.
    - quality: The compression quality (0 to 100, where 0 is the highest compression and 100 is the best quality).

    Returns:
    - BytesIO: In-memory buffer containing the compressed image.
    """
    with Image.open(image_data) as img:

        # resize image
        img.thumbnail((351, 351))

        # compress image
        image_buffer = BytesIO()
        img.save(image_buffer, 'PNG', quality=quality)
        image_buffer.seek(0)
        
        return image_buffer
    
def get_leaderboard():
    '''
    Get the leaderboard
    '''
    leaderboard = db_session.query(Players).order_by(Players.wins.desc())
    return [[player.name, player.wins] for player in leaderboard]

import firebase_admin
from firebase_admin import credentials
from firebase_admin.storage import bucket

# init the firebase admin
cred = credentials.Certificate("./service-account.json")
firebase_admin.initialize_app(cred,{'storageBucket': 'facial-frenzy.appspot.com'})

def upload_image_to_firebase(image_file, destination_path):
    '''
    Example Usage:
    ```
    id = str(uuid.uuid4().hex)[:8]
    img = Image.open('./data/johno1.png')
    img.save(f'{id}.{img.format}')
    upload_image_to_firebase(f'{id}.{img.format}', f'faces/1/{id}')
    image = download_image_from_firebase(f'faces/1/{id}')
    image.show()
    os.remove(f'{id}.{img.format}')
    ```
    '''
    try:
        # init bucket obj

        buc = bucket()
        blob = buc.blob(destination_path)
        blob.upload_from_file(image_file)

    except AuthError as e:
        print(f"Error: {e}")
    except ApiError as e:
        print(f"API Error: {e}")

def upload_image_path_to_firebase(image_path, destination_path):
    '''
    Example Usage:
    ```
    id = str(uuid.uuid4().hex)[:8]
    img = Image.open('./data/johno1.png')
    img.save(f'{id}.{img.format}')
    upload_image_to_firebase(f'{id}.{img.format}', f'faces/1/{id}')
    image = download_image_from_firebase(f'faces/1/{id}')
    image.show()
    os.remove(f'{id}.{img.format}')
    ```
    '''
    try:
        # init bucket obj

        buc = bucket()
        blob = buc.blob(destination_path)
        blob.upload_from_filename(image_path)

    except AuthError as e:
        print(f"Error: {e}")
    except ApiError as e:
        print(f"API Error: {e}")

def download_image_from_firebase(source_path):
    '''
    Example Usage:
    ```
    id = str(uuid.uuid4().hex)[:8]
    img = Image.open('./data/johno1.png')
    img.save(f'{id}.{img.format}')
    upload_image_to_firebase(f'{id}.{img.format}', f'faces/1/{id}')
    image = download_image_from_firebase(f'faces/1/{id}')
    image.show()
    os.remove(f'{id}.{img.format}')
    ```
    '''
    try:
        # init dropbox cli

        buc = bucket()
        blob = buc.blob(source_path)
        image_data = blob.download_as_bytes()

        # return img
        return Image.open(BytesIO(image_data))
    except AuthError as e:
        print(f"Error: {e}")
    except ApiError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
