from configparser import ConfigParser
from os import getenv
from PyQt6.QtGui import QFont


def get_api_key():
    api_key = getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    return api_key


class Config:
    def __init__(self, config_file="config.ini"):
        self.cfg = ConfigParser()
        self.cfg.read(config_file)

        self.GPT3_MODEL = self.cfg["OPENAI"]["GPT3_MODEL"]
        self.GPT4_MODEL = self.cfg["OPENAI"]["GPT4_MODEL"]
        self.FREQ_PENALTY = self.cfg.getfloat("OPENAI", "FREQ_PENALTY")
        self.CHAT_TEMP = self.cfg.getfloat("OPENAI", "CHAT_TEMP")
        self.TUTOR_TEMP = self.cfg.getfloat("OPENAI", "TUTOR_TEMP")
        self.IMG_MODEL = self.cfg["OPENAI"]["IMG_MODEL"]
        self.IMG_SIZE = self.cfg["OPENAI"]["IMG_SIZE"]
        self.QUALITY = self.cfg["OPENAI"]["QUALITY"]
        self.VISION_MODEL = self.cfg["OPENAI"]["VISION_MODEL"]
        self.WHISPER_MODEL = self.cfg["OPENAI"]["WHISPER_MODEL"]
        self.TTS_MODEL = self.cfg["OPENAI"]["TTS_MODEL"]
        self.TTS_VOICE = self.cfg["OPENAI"]["TTS_VOICE"]
        self.MAX_TOKENS = self.cfg.getint("OPENAI", "MAX_TOKENS")
        self.speech_file_path = self.cfg["PATH"]["speech_file_path"]
        self.clipboard_path = self.cfg["PATH"]["clipboard_path"]
        self.version = self.cfg["OTHER"]["version"]
        self.api_key = get_api_key()
        self.BTN_WIDTH = 80
        self.TUTOR_INPUT_HT = 30
        self.USER_INPUT_HT = 100
        self.ASST_RESP_HT = 300
        self.ASST_FONT = QFont("Menlo", 13)
        self.DEFAULT_FONT = QFont("Arial", 14)
        self.help_file = "help.txt"

    def reload_config(self):
        self.ASST_FONT = QFont("Menlo", 13)
        self.DEFAULT_FONT = QFont("Arial", 14)