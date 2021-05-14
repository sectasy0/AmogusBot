from json import loads
from typing import List

class Sigleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Sigleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Settings(metaclass=Sigleton):
    def __init__(self, app_token: str, cmd_prefix: str, tasks: List[str]) -> None:
        self._app_token: str = app_token
        self._cmd_prefix: str = cmd_prefix
        self._tasks: List[str] = tasks

    @classmethod
    def from_json(cls, json_dict: dict = "settings.json") -> object:
        with open(json_dict, 'r') as file:
            return cls(**loads(file.read()))

    @property
    def app_token(self) -> str:
        return self._app_token

    @property
    def cmd_prefix(self) -> str:
        return self._cmd_prefix
    
    @property
    def tasks(self) -> str:
        return self._tasks