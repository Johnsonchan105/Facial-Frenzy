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

@app.route('/api/getplayer')
def getplayer():
    '''
    This route returns the player object in the db given a name, gamertag, or id
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

    print(name, gamertag, user_id)

    # get player from db
    try:
        player = None
        if name:
            player = utils.get_player_by_name_from_db(name)
        elif gamertag:
            player = utils.get_player_by_tag_from_db(gamertag)
        elif user_id:
            player = utils.get_player_by_id_from_db(user_id)
        print(player)
        return jsonify(
                id=player.user_id,
                name=player.name,
                gamertag=player.gamertag,
                wins=gamertag.wins), 200
    except Exception as e:
        print(f"Exception in postlog: {e}")
        return {'MESSAGE': f"Exception in /api/getplayer {e}"}, 401 