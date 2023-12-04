import sys
import sys
sys.path.append("..")
sys.path.append("../emotion_reg")
from io import BytesIO
import requests
from face_recognizer.main import FaceRecognition
from emotion_reg.emotionreg import EmotionGame
import asyncio
from PIL import Image

API_ENDPOINT = 'http://169.231.155.196:8000' # 'http://localhost:8000'

def compress_image(image_data, quality=85):
    """
    Compress an image in a Flask FileStorage object with Pillow.

    Parameters:
    - file_storage: Flask FileStorage object representing the input image.
    - quality: The compression quality (0 to 100, where 0 is the highest compression and 100 is the best quality).

    Returns:
    - BytesIO: In-memory buffer containing the compressed image.
    """

    # resize image
    img.thumbnail((500, 500))

    # compress image
    image_buffer = BytesIO()
    img.save(image_buffer, 'PNG', quality=quality)
    image_buffer.seek(0)
    
    return image_buffer
    
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

def get_player(name, verbose=True):

    PATH = '/api/getplayer'
    endpoint = API_ENDPOINT + PATH

    res = requests.get(endpoint, json={'name': name})

    content = res.json()

    if res.status_code != 200:
        # player doesnt exist. make a new one
        create_player(name)
        
        PATH = '/api/getplayer'
        endpoint = API_ENDPOINT + PATH

        res = requests.get(endpoint, json={'name': name})

        return res.json()
    if verbose:
        print(f'WELCOME BACK {name}!')
    
    return content

def update_score(user_id, score):
    print('TEST: UPDATE PLAYER SCORE')

    PATH = '/api/updatescore'
    endpoint = API_ENDPOINT + PATH

    res = requests.post(endpoint, json={'user_id': user_id, 'points': score})

    content = res.json()

def post_face(user_id, image_data):

    PATH = f'/api/postface/{user_id}'
    endpoint = API_ENDPOINT + PATH


    files = { 'face': image_data }

    _ = requests.post(endpoint, files=files)

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

    emo_game = EmotionGame()
    emo_game.run_game()

    # get player score
    score = emo_game.score

    update_score(player['id'], score)
    print('Your new score is:', get_player(player['name'], verbose=False)['wins'])

    for image in emo_game.pictures:
        img = Image.fromarray(image)
        img = compress_image(img)
        # Image.open(img).show()
        post_face(player['id'], img)

    print('Your pictures have been uploaded! Check out your profile.')