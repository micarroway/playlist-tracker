import json
from os.path import realpath, dirname

"""
The AppConfig class has a single static variable that gets loaded only one time and kept in memory.
We can then reference AppConfig.config anywhere and be guaranteed the same config file

Static variables are variables that are shared across ALL instances of a class. If you modify a static 
variable in one instance of a class all other instances will have that new value.
"""


class AppConfig:
    config = json.load(open(dirname(realpath(__file__)) + '/../app_config.json'))
