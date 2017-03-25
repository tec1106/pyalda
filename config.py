'''Pyalda config'''

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

RUN = {
    'debug':True,
    'port':5000,
    'host':'0.0.0.0'
}
