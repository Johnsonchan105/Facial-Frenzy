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

def postface():
    print('TEST: POST PLAYER IMAGE')

    path = '/api/postface/1'
    endpoint = url + path

    img = Image.open('./data/johno1.png')

    files = { 'face': open('./data/johno1.png', 'rb') }

    headers = {'content-type': 'image/png'}

    res = requests.post(endpoint, data={'expression': 'hi'}, files=files)

    content = res.json()
    print(content, res.status_code)


if __name__ == "__main__":
    # getplayer()
    # createplayer()
    # updatescore()
    postface()
    

    
