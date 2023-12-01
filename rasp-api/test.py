import requests
from datetime import datetime, timedelta, timezone
import os, sys, dotenv, random, string, argparse
from utils import upload_image_to_dropbox
import uuid
import dropbox
from dropbox.exceptions import AuthError, ApiError

url = 'http://localhost:8000'

dotenv.load_dotenv() #set the environment variables from .env file

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_APP_ACCESS_TOKEN")

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

if __name__ == "__main__":
    # getplayer()
    # createplayer()
    # updatescore()
    upload_image_to_dropbox('./data/johno1.png', f'/faces/1/{str(uuid.uuid4().hex)[:8]}')