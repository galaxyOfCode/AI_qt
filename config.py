from configparser import ConfigParser
from os import getenv
from PyQt6.QtGui import QFont


def get_api_key() -> str:
    api_key = getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    return api_key


class Config:
    def __init__(self, config_file="config.ini") -> None:
        self.cfg = ConfigParser()
        self.cfg.read(config_file)

        self.MODEL_LIST = self.cfg["OPENAI"]["MODEL_LIST"].split(", ")
        self.IMG_MODEL = self.cfg["OPENAI"]["IMG_MODEL"]
        self.IMG_SIZE = self.cfg["OPENAI"]["IMG_SIZE"]
        self.QUALITY = self.cfg["OPENAI"]["QUALITY"]
        self.WHISPER_MODEL = self.cfg["OPENAI"]["WHISPER_MODEL"]
        self.TTS_MODEL = self.cfg["OPENAI"]["TTS_MODEL"]
        self.TTS_VOICE = self.cfg["OPENAI"]["TTS_VOICE"]
        self.MAX_TOKENS = self.cfg.getint("OPENAI", "MAX_TOKENS")
        self.speech_file_path = self.cfg["PATH"]["speech_file_path"]
        self.clipboard_path = self.cfg["PATH"]["clipboard_path"]
        self.version = self.cfg["OTHER"]["version"]
        self.api_key = get_api_key()
        self.BTN_WIDTH = 80
        self.USER_INPUT_HT = 100
        self.ASST_RESP_HT = 300
        self.ASST_FONT = QFont("Menlo", 13)
        self.DEFAULT_FONT = QFont("Arial", 14)
        self.help_file = "help.txt"

    def reload_config(self) -> None:
        self.ASST_FONT = QFont("Menlo", 13)
        self.DEFAULT_FONT = QFont("Arial", 14)