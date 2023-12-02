import sys
import sys
sys.path.append("..")
sys.path.append("../emotion_reg")

import requests
from face_recognizer.main import FaceRecognition
from emotion_reg.emotionreg import EmotionGame
import asyncio

API_ENDPOINT = 'http://localhost:8000'

def login_player():
    fr = FaceRecognition()
    player_name = asyncio.run(fr.run_recognition())
    return player_name

def create_player(name):

    PATH = '/api/createplayer'
    endpoint = API_ENDPOINT + PATH

    res = requests.post(endpoint, json={'name': name, 'gamertag': name})

    content = res.json()

    print(f'WE NOTICED YOU ARE NEW HERE {name}. WELCOME!')

    return content

def get_player(name):

    PATH = '/api/getplayer'
    endpoint = API_ENDPOINT + PATH

    res = requests.get(endpoint, json={'name': name})

    content = res.json()

    if res.status_code != 200:
        # player doesnt exist. make a new one
        return create_player(name)
    
    print(f'WELCOME BACK {name}!')
    
    return content

def update_score(user_id, score):
    print('TEST: UPDATE PLAYER SCORE')

    PATH = '/api/updatescore'
    endpoint = API_ENDPOINT + PATH

    res = requests.post(endpoint, json={'user_id': user_id, 'points': score})

    content = res.json()

    print(content, res.status_code)

if __name__ == "__main__":
    print('THIS IS FACIAL FRENZY')
    print('SHALL WE PLAY A GAME? (y/n)')
    start = input()
    if start.lower() == 'n' or start.lower() == 'no':
        print('PLEASE PLAY AGAIN')
        sys.exit()
    
    player_name = login_player()
    
    # get the player obj from the db
    player = get_player(player_name)

    # emo_game = EmotionGame()
    # emo_game.run_game()

    # get player score
    score = 10 # emo_game.score

    update_score(player['id'], score)
    print('Your new score is:', get_player(player['name'])['wins'])
