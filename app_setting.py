import os


PUBLIC_KEY = 'This is an IV456'
CHECK_CYPHER = b'I33UYA8Ec6jGJ6PU5WV3nQ=='

BASE_DIR = os.getcwd()

TEMPLATE_DIR = os.path.join(BASE_DIR, 'web/templates')

if os.environ.get('GAE_INSTANCE'):
    DB_CONNECTION_DICT = {
        'host': 'localhost',
        'user': 'user1',
        'passwd': 'asdqwe',
        'db': 'remote_test'
    }
else:
    DB_CONNECTION_DICT = {
        'host': 'localhost',
        'user': 'user1',
        'passwd': 'asdqwe',
        'db': 'remote_test'
    }

