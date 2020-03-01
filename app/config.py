import os
import json

_basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEV_MODE = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    if DEV_MODE:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
