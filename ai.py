from os import getenv
import sys
import configparser
from openai import OpenAI
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QFileDialog
from chat import chat
from code_review import code_review
from image import vision, image
from ui_components import MainFrame, ButtonFrame, RadioFrame
from utilities import get_model_names, get_settings
from voice import tts, whisper

cfg = configparser.ConfigParser()
cfg.read("config.ini")

GPT3_MODEL = cfg["OPENAI"]["GPT3_MODEL"]
GPT4_MODEL = cfg["OPENAI"]["GPT4_MODEL"]
CODE_REVIEW_MODEL = cfg["OPENAI"]["GPT4_MODEL"]
FREQ_PENALTY = float(cfg["OPENAI"]["FREQ_PENALTY"])
CHAT_TEMP = float(cfg["OPENAI"]["CHAT_TEMP"])
TUTOR_TEMP = float(cfg["OPENAI"]["TUTOR_TEMP"])
IMG_MODEL = cfg["OPENAI"]["IMG_MODEL"]
QUALITY = cfg["OPENAI"]["QUALITY"]
VISION_MODEL = cfg["OPENAI"]["VISION_MODEL"]
WHISPER_MODEL = cfg["OPENAI"]["WHISPER_MODEL"]
TTS_MODEL = cfg["OPENAI"]["TTS_MODEL"]
TTS_VOICE = cfg["OPENAI"]["TTS_VOICE"]
MAX_TOKENS = float(cfg["OPENAI"]["MAX_TOKENS"])
FONT_FAMILY = cfg["UI"]["FONT_FAMILY"]
FONT_SIZE = int(cfg["UI"]["FONT_SIZE"])
DEFAULT_FONT = QFont(FONT_FAMILY, FONT_SIZE)

api_key = getenv("OPENAI_API_KEY")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()
        self.default_font_norm = DEFAULT_FONT
        self.setFont(self.default_font_norm)
        self.default_font_bold = DEFAULT_FONT
        self.default_font_bold.setBold(True)
        self.setGeometry(100, 50, 900, 500)
        self.setWindowTitle("AI Assistant")
        self.clipboard = QApplication.clipboard()

        # Create a layout
        self.grid = QGridLayout()

        # Create frames
        self.mainframe = MainFrame()
        self.radioframe = RadioFrame(self.mainframe)
        self.buttonframe = ButtonFrame(self.mainframe)

        # Add frames to the layout
        self.grid.addWidget(self.radioframe, 0, 0)
        self.grid.addWidget(self.buttonframe, 1, 0)
        self.grid.addWidget(self.mainframe, 0, 1, 2, 1)

        # Set Enter button action
        self.buttonframe.enter_btn.clicked.connect(self.on_enter_click)

        # Set layout
        self.setLayout(self.grid)
        self.mainframe.user_input.setFocus()

    def no_prompt(self, box) -> None:
        """Error message when no user prompt detected"""
        self.mainframe.asst_resp.setPlainText(
            f"Please enter a prompt in the '{box}:' box")
        self.buttonframe.enter_btn.setEnabled(True)

    def is_user_input_required(self) -> bool:
        """ Is text field required for the selected radio button"""
        checked_buttons = ["Chat 3.5", "Chat 4.0", "Tutor 3.5",
                           "Tutor 4.0", "Image Gen", "Text-to-Speech"]
        rb = self.radioframe.get_checked_radio_button()
        return rb in checked_buttons

    def is_tutor_input_required(self) -> bool:
        """ Is text field required for the selected radio button"""
        rb = self.radioframe.get_checked_radio_button()
        return rb == "Tutor 3.5" or rb == "Tutor 4.0"

    def get_file_name(self) -> str:
        """ Gets a file name to pass along to one of the openAI functions """
        file = QFileDialog.getOpenFileName(None, "Select a File")
        return "" if file == "" else file[0]

    def set_response(self, content) -> None:
        """Implement setting the response in the UI"""
        rb = self.radioframe.get_checked_radio_button()
        if rb == "Image Gen":
            self.mainframe.asst_resp.setHtml(
                f"<a href='{content}'>{content}</a>")
        else:
            self.mainframe.asst_resp.clear()
            self.mainframe.asst_resp.setPlainText(content)

    def on_enter_click(self) -> None:
        """Execute function associated with selected radio button"""
        self.buttonframe.enter_btn.setEnabled(False)
        self.mainframe.asst_resp.setPlainText("Processing . . .")
        text = self.mainframe.user_input.toPlainText()
        tutor = self.mainframe.tutor_input.toPlainText()

        if not text and self.is_user_input_required():
            self.no_prompt("User")
            return

        if not tutor and self.is_tutor_input_required():
            self.no_prompt("Tutor")
            return

        action_mapping = {
            self.radioframe.radio_buttons[0]: lambda: chat(self.client, GPT3_MODEL, CHAT_TEMP, FREQ_PENALTY, 1, text),
            self.radioframe.radio_buttons[1]: lambda: chat(self.client, GPT4_MODEL, CHAT_TEMP, FREQ_PENALTY, 1, text),
            self.radioframe.radio_buttons[2]: lambda: chat(self.client, GPT3_MODEL, TUTOR_TEMP, FREQ_PENALTY, 0, text, tutor),
            self.radioframe.radio_buttons[3]: lambda: chat(self.client, GPT4_MODEL, TUTOR_TEMP, FREQ_PENALTY, 0, text, tutor),
            self.radioframe.radio_buttons[4]: lambda: code_review(self.client, GPT4_MODEL, self.get_file_name()),
            self.radioframe.radio_buttons[5]: lambda: image(self.client, IMG_MODEL, QUALITY, text),
            self.radioframe.radio_buttons[6]: lambda: vision(api_key, VISION_MODEL, MAX_TOKENS, self.get_file_name()),
            self.radioframe.radio_buttons[7]: lambda: whisper(self.client, WHISPER_MODEL, self.get_file_name()),
            self.radioframe.radio_buttons[8]: lambda: tts(self.client, TTS_MODEL, TTS_VOICE, text),
            self.radioframe.radio_buttons[9]: lambda: get_model_names(self.client, 1),
            self.radioframe.radio_buttons[10]: lambda: get_model_names(self.client, 0),
            self.radioframe.radio_buttons[11]: lambda: get_settings(),
        }

        for rb, action in action_mapping.items():
            if rb.isChecked():
                content = action()
                break

        self.set_response(content)
        self.clipboard.setText(content)
        self.buttonframe.enter_btn.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
