import os
import socket
from pathlib import Path

from dotenv import dotenv_values


class Config:
    def __init__(self):
        self.ROOT_PATH = Path(__file__).parent.parent.parent
        self.ENV_PATH = self.ROOT_PATH / ".env"
        self._load_user()
        self._load_env()

    def _load_user(self):
        self.USERNAME = os.getlogin()
        self.HOSTNAME = socket.getfqdn()

    def _load_env(self):
        self.env = dotenv_values(self.ENV_PATH)
