import json
from os.path import realpath, dirname


class AppConfig:
    config = json.load(open(dirname(realpath(__file__)) + '/../app_config.json'))
