import requests
from datetime import datetime, timedelta, timezone
import os, sys, dotenv, random, string, argparse
import uuid
import dropbox
from dropbox.exceptions import AuthError, ApiError
from dropbox import DropboxOAuth2FlowNoRedirect
import os.path
from PIL import Image
from io import BytesIO

import firebase_admin
from firebase_admin import credentials
from firebase_admin.storage import bucket
import tempfile

# init the firebase admin
cred = credentials.Certificate("./service-account.json")
firebase_admin.initialize_app(cred,{'storageBucket': 'facial-frenzy.appspot.com'})


url = 'http://localhost:8000'

dotenv.load_dotenv() #set the environment variables from .env file

def getplayer():
    print('TEST: GET PLAYER')

    path = '/api/getplayer'
    endpoint = url + path

    res = requests.get(endpoint, json={'name': 'Cap'})

    content = res.json()
    
    print(content, res.status_code)

def createplayer():
    print('TEST: CREATE PLAYER')

    path = '/api/createplayer'
    endpoint = url + path

    res = requests.post(endpoint, json={'name': 'NEWPLAYER', 'gamertag': 'HOGRIDER'})

    content = res.json()
    print(content, res.status_code)

def updatescore():
    print('TEST: UPDATE PLAYER SCORE')

    path = '/api/updatescore'
    endpoint = url + path

    res = requests.post(endpoint, json={'user_id': 1})

    content = res.json()
    print(content, res.status_code)
    
def upload_image_to_firebase(image_path, destination_path):
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
    try:
        # init dropbox cli

        buc = bucket()
        blob = buc.blob(source_path)
        image_data = blob.download_as_string()

        # return img
        return Image.open(BytesIO(image_data))
    except AuthError as e:
        print(f"Error: {e}")
    except ApiError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # getplayer()
    # createplayer()
    # updatescore()
    id = str(uuid.uuid4().hex)[:8]
    img = Image.open('./data/johno1.png')
    img.save(f'{id}.{img.format}')
    upload_image_to_firebase(f'{id}.{img.format}', f'faces/1/{id}')
    image = download_image_from_firebase(f'faces/1/{id}')
    image.show()
    os.remove(f'{id}.{img.format}')

    
