import configparser
import os
from PyQt6.QtGui import QFont

class Config:
    def __init__(self, config_file='config.ini'):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_file)
        self.load_settings()

    def load_settings(self):
        self.GPT3_MODEL = self.cfg["OPENAI"]["GPT3_MODEL"]
        self.GPT4_MODEL = self.cfg["OPENAI"]["GPT4_MODEL"]
        self.CODE_REVIEW_MODEL = self.cfg["OPENAI"]["GPT4_MODEL"]
        self.FREQ_PENALTY = self.cfg.getfloat("OPENAI", "FREQ_PENALTY")
        self.CHAT_TEMP = self.cfg.getfloat("OPENAI", "CHAT_TEMP")
        self.TUTOR_TEMP = self.cfg.getfloat("OPENAI", "TUTOR_TEMP")
        self.IMG_MODEL = self.cfg["OPENAI"]["IMG_MODEL"]
        self.QUALITY = self.cfg["OPENAI"]["QUALITY"]
        self.VISION_MODEL = self.cfg["OPENAI"]["VISION_MODEL"]
        self.WHISPER_MODEL = self.cfg["OPENAI"]["WHISPER_MODEL"]
        self.TTS_MODEL = self.cfg["OPENAI"]["TTS_MODEL"]
        self.TTS_VOICE = self.cfg["OPENAI"]["TTS_VOICE"]
        self.MAX_TOKENS = self.cfg.getint("OPENAI", "MAX_TOKENS")
        self.FONT_FAMILY = self.cfg["UI"]["FONT_FAMILY"]
        self.FONT_SIZE = self.cfg.getint("UI", "FONT_SIZE")
        self.DEFAULT_FONT = QFont(self.FONT_FAMILY, self.FONT_SIZE)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.BTN_WIDTH = self.cfg.getint("UI", "BTN_WIDTH")
        self.TUTOR_INPUT_HT = self.cfg.getint("UI", "TUTOR_INPUT_HT")
        self.USER_INPUT_HT = self.cfg.getint("UI", "USER_INPUT_HT")
        self.ASST_RESP_HT = self.cfg.getint("UI", "ASST_RESP_HT")
        self.ASST_FONT_FAMILY = self.cfg["UI"]["ASST_FONT_FAMILY"]
        self.ASST_FONT_SIZE = self.cfg.getint("UI", "ASST_FONT_SIZE")
        self.ASST_FONT = QFont(self.ASST_FONT_FAMILY, self.ASST_FONT_SIZE)
