from __main__ import app
import sys, os
from datetime import timedelta, datetime, timezone
from flask import request, jsonify, render_template, send_file
import utils
import uuid
import io
#import the flask-jwt-extended interface in the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'flask-jwt-extended'))

DEBUG=True

myname = os.environ.get("ME")

# create a default route
@app.route('/')
def hello():
    ''' 
    This route prints the welcome message using the myname variable passed in as an environment variable.
    '''
    return f'Welcome to Facial Frenzy from {myname}\n', 200

@app.route('/api/getplayer', methods=['GET'])
def getplayer():
    '''
    This route returns the player object in the db given a name, gamertag, or id.
    '''
    # parse params
    params = None
    if request.args:
        params = request.args
    elif request.json: 
        params = request.json
    elif request.form: 
        params = request.form

    # extract param values
    name = params.get('name', None)
    gamertag = params.get('gamertag', None)
    user_id = params.get('user_id', None)

    # get player from db
    try:
        player = None
        if name:
            player = utils.get_player_by_name_from_db(name)
        elif gamertag:
            player = utils.get_player_by_tag_from_db(gamertag)
        elif user_id:
            player = utils.get_player_by_id_from_db(user_id)

        if not player:
            return jsonify({'MESSAGE': f"Player doesn't exist."}), 401 
 
        return jsonify(
                id=player.user_id,
                name=player.name,
                gamertag=player.gamertag,
                wins=player.wins), 200
    except Exception as e:
        print(f"Exception in postlog: {e}")
        return jsonify({'MESSAGE': f"Exception in /api/getplayer {e}"}), 401 
    
@app.route('/api/createplayer', methods=['POST'])
def createplayer():
    '''
    This route creates a new player object in the db.
    '''
    # parse params
    params = None
    if request.args:
        params = request.args
    elif request.json: 
        params = request.json
    elif request.form: 
        params = request.form

    # extract param values
    name = params.get('name', None)
    gamertag = params.get('gamertag', None)

    # add player from db
    try:        
        if name and gamertag:
            utils.add_player_to_db(name, gamertag)
        else:
            return {'MESSAGE': 'Missing arguments'}, 401
        
        return {'MESSAGE': 'Successfully added player'}, 200
    except Exception as e:
        print(f"Exception in postlog: {e}")
        return {'MESSAGE': f"Exception in /api/createplayer {e}"}, 401 
    
@app.route('/api/updatescore', methods=['POST'])
def updatescore():
    '''
    This route updates a player's win count in the db.
    Requires user_id.
    '''
     # parse params
    params = None
    if request.args:
        params = request.args
    elif request.json: 
        params = request.json
    elif request.form: 
        params = request.form

    user_id = params.get('user_id', None)
    points = params.get('points', None)
    if not user_id and not points:
        return {'MESSAGE': 'Missing arguments'}, 401
    try:
        if user_id:
            utils.update_player_score(user_id, points)
        return {'MESSAGE': f"Successfully updated player score"}, 200 
    except Exception as e:
        print(f"Exception in postlog: {e}")
        return {'MESSAGE': f"Exception in /api/updatescore {e}"}, 401 

@app.route('/api/postface/<int:user_id>', methods=['POST'])
def postface(user_id):
    '''
    This route adds a photo for a user.
    Requires user_id.
    '''
    
    if 'face' not in request.files:
        return {'MESSAGE': 'Missing image'}, 401
    else:
        file = request.files['face']

    try:
        uid = str(uuid.uuid4().hex)[:8]
        storage_path = f'faces/{user_id}/{uid}'
        file = utils.compress_image(file, 20)
        utils.upload_image_to_firebase(file, storage_path)
        utils.add_player_image(user_id, storage_path)
        image = utils.download_image_from_firebase(storage_path)

        return {'MESSAGE': f"Successfully uploaded player image"}, 200 
        
    except Exception as e:
        print(f"Exception in postlog: {e}")
        return {'MESSAGE': f"Exception in /api/updatescore {e}"}, 401 

@app.route('/player/<int:user_id>', methods=['GET'])
def getallfaces(user_id):
    '''
    This route displays a player and their game info
    Requires user_id.
    '''
    try:
        player = utils.get_player_by_id_from_db(user_id)
        image_paths = utils.get_player_images_paths(user_id)

        return render_template('player.html', player=player.name, wins=player.wins, images=image_paths)

        return {'MESSAGE': f"Successfully uploaded player image"}, 200 
        
    except Exception as e:
        print(f"Exception in postlog: {e}")
        return {'MESSAGE': f"Exception in /api/updatescore {e}"}, 401 
    
@app.route('/player/faces/<int:user_id>/<string:uid>', methods=['GET'])
def getface(user_id, uid):
    image = utils.download_image_from_firebase(f'faces/{user_id}/{uid}') 
    image_data = io.BytesIO()
    image.save(image_data, format='PNG')
    image_data.seek(0)
    return send_file(image_data, mimetype='image/png')

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    leaderboard = utils.get_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard)
