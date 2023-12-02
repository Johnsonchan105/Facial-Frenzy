import sys
import requests

def login_player():
    pass

if __name__ == "__main__":
    print('WELCOME TO FACIAL FRENZY')
    print('SHALL WE PLAY A GAME? (y/n)')
    start = input()
    if start.lower() == 'n' or start.lower() == 'no':
        print('PLEASE PLAY AGAIN')
        sys.exit()
    
    player_name = login_player()


    
