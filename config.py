"""Configuration management for AI Assistant application."""

from configparser import ConfigParser
from os import getenv
from PyQt6.QtGui import QFont


def get_api_key() -> str:
    """Retrieve the OpenAI API key from environment variables."""
    api_key = getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    return api_key


class Config:
    """Configuration management for AI Assistant application."""
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern to ensure only one instance of Config exists."""
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_file="config.ini") -> None:
        """Initialize the configuration settings."""
        if self._initialized:
            return

        self.cfg = ConfigParser()
        self.cfg.read(config_file)

        self.MODEL_LIST = self.cfg["OPENAI"]["MODEL_LIST"].split(", ")
        self.IMG_MODEL = self.cfg["OPENAI"]["IMG_MODEL"]
        self.IMG_SIZE = self.cfg["OPENAI"]["IMG_SIZE"]
        self.VISION_MODEL = self.cfg["OPENAI"]["VISION_MODEL"]
        self.TRANSCRIBE_MODEL = self.cfg["OPENAI"]["TRANSCRIBE_MODEL"]
        self.TTS_MODEL = self.cfg["OPENAI"]["TTS_MODEL"]
        self.TTS_VOICE = self.cfg["OPENAI"]["TTS_VOICE"]
        self.MAX_TOKENS = self.cfg.getint("OPENAI", "MAX_TOKENS")
        self.speech_file_path = self.cfg["PATH"]["speech_file_path"]
        self.image_path = self.cfg["PATH"]["image_file_path"]
        self.clipboard_path = self.cfg["PATH"]["clipboard_path"]
        self.version = self.cfg["OTHER"]["version"]
        self.api_key = get_api_key()
        self.BTN_WIDTH = 80
        self.USER_INPUT_HT = 100
        self.ASST_RESP_HT = 300
        self.ASST_FONT = QFont("Menlo", 13)
        self.DEFAULT_FONT = QFont("Arial", 14)
        self.help_file = "help.txt"

        self._initialized = True

    def reload_config(self) -> None:
        """Reload the configuration settings."""
        self.ASST_FONT = QFont("Menlo", 13)
        self.DEFAULT_FONT = QFont("Arial", 14)
