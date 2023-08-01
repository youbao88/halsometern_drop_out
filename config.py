import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = '41f751c417b875d152227df3e816437c'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db') 
    LANGUAGES = ['sv', 'en']
    BABEL_DEFAULT_LOCALE = 'en'