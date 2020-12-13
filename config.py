import json

from meta.singleton import Singleton


class Configuration(metaclass=Singleton):
    def __init__(self, name):
        with open(name, "r") as file:
            self.config = json.load(file)