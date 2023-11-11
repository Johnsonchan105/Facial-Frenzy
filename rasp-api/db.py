import os, sys, dotenv, argparse, random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

dotenv.load_dotenv() #set the environment variables from .env file
uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
engine = create_engine(uri)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

# import utils and model that depend on db_session
import utils
from models import Base

def init_db(cleandb=False):
    if not cleandb:
        Base.metadata.create_all(bind=engine)
    else:
        print('cleaning out the DB!')
        import db_init_data
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        print('adding data, this might take a while...')

        # create players, games, face finishers
        utils.add_players_in_list_to_db(db_init_data.players_list)

    print('The database has been checked and all models have been installed without error.')

def main():
    parser = argparse.ArgumentParser(description='Running this file directly either cleans out the DB and resets it for lab3 (-c flag) or checks that the DB is setup and ready to go for lab3 (no args). The program should exit without errors.') 
    parser.add_argument('--cleandb','-c',action='store_true',
        help='set this if you want to clear out the database (all tables) and start from scratch with the lab3 seed data')
    args = parser.parse_args()
    init_db(args.cleandb)

if __name__ == "__main__":
    main()