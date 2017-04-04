'''Pyalda config'''
import os
base_dir = os.path.dirname(os.path.realpath(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'app', 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

'''
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:turtle@localhost/knektdev'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_BINDS = {
    'foo':'sqlite:///' + os.path.join(basedir, 'foo.db'),
}
'''

SECRET_KEY = '84 8b 81 a0 42 d5 ce 61 1f 1a'

RUN = {
    'debug':True,
    'port':5000,
    'host':'127.0.0.1'
}
