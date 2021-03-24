import ast
import os
import redis

from src.config import CONFIGS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'g+ymsxys8rqol5=4&7s6nom5d8p4=iavmt8nn&^y0wlj9o$aii'

DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'True'))

hostname = os.popen('hostname').read().replace('\n', '')

release_hostname = ['localhost.localdomain']

if hostname in release_hostname:
    DEBUG = False

elif not CONFIGS.__contains__(hostname):
    hostname = 'dev'

PROFILES = CONFIGS[hostname]

LOG_FILE_PATH = os.path.join(BASE_DIR, 'log')

if not os.path.exists(LOG_FILE_PATH):
    os.makedirs(LOG_FILE_PATH)

# REDIS_INFO = PROFILES['REDIS']
#
# redis = redis.Redis(host=REDIS_INFO['HOST'], port=REDIS_INFO['PORT'], password=REDIS_INFO['PASSWORD'])

BASE_URL = PROFILES['BASE_URL']

File_Types = ['img', 'video', 'file']

WHITE_HOSTS = ['127.0.0.1',]
