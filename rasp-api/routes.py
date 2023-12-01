from __main__ import app
import sys, os
from datetime import timedelta, datetime, timezone
from flask import request, jsonify
import utils
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
    return f'Welcome to CS190B Sensors Hub from {myname}\n', 200

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
    if not user_id:
        return {'MESSAGE': 'Missing arguments'}, 401
    try:
        if user_id:
            utils.update_player_score(user_id)
        return {'MESSAGE': f"Successfully updated player score"}, 200 
    except Exception as e:
        print(f"Exception in postlog: {e}")
        return {'MESSAGE': f"Exception in /api/updatescore {e}"}, 401 

@app.route('/api/addphoto', methods=['POST'])
def addphoto():
    '''
    This route adds a photo for a user.
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

    if not user_id:
        return {'MESSAGE': 'Missing arguments'}, 401
    try:
        if user_id:
            utils.update_player_score(user_id)
        return {'MESSAGE': f"Successfully updated player score"}, 200 
    except Exception as e:
        print(f"Exception in postlog: {e}")
        return {'MESSAGE': f"Exception in /api/updatescore {e}"}, 401 