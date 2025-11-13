from sqlalchemy import create_engine
import urllib
import os
from dotenv import load_dotenv
load_dotenv()

user = os.environ['DB_USER']
password = urllib.parse.quote_plus(os.environ['DB_PASSWORD'])
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
database = os.environ['DB_DATABASE']


def get_engine():

    """
    Connect to SQLServer database
    """

    connect_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user,password,host,port,database)
    print(connect_string)
    try:
        engine = create_engine(connect_string, echo=False)
        return engine
    except Exception as e:
        print(f'Failed to connect {host}:{database}')
        raise
