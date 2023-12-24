from os import getenv
import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QRadioButton, QPushButton, QLabel, QTextEdit, QFileDialog
from openai import OpenAI

from chat import chat
from code_review import code_reviewer
from image import vision, image
from voice import tts, whisper
from help import help_text

BTN_WIDTH = 80
FONT_SIZE = 14
FONT = "Arial"
TUTOR_INPUT_HT = 30
USER_INPUT_HT = 100
ASST_RESP_HT = 300

GPT3_MODEL = "gpt-3.5-turbo-1106"
GPT4_MODEL = "gpt-4-1106-preview"
CODE_REVIEW_MODEL = "gpt-4-1106-preview"
FREQ_PENALTY = .4
CHAT_TEMP = .8
TUTOR_TEMP = .2
IMG_MODEL = "dall-e-3"
SIZE = "1024x1024"
STYLE = "vivid"
VISION_MODEL = "gpt-4-vision-preview"
WHISPER_MODEL = "whisper-1"
TTS_MODEL = "tts-1-1106"
TTS_VOICE = "echo"
MAX_TOKENS = 4000

api_key = getenv("OPENAI_API_KEY")

def get_model_names(client, option):
    '''List only the GPT models available through the API'''

    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    if option == 1:
        model_ids = [
            model_id for model_id in model_ids if model_id.startswith("gpt")]
    model_ids.sort()
    if option == 1:
        header = "Current openAI GPT Models:\n\n"
    else:
        header = "Current openAI Models:\n\n"
    content = ("\n".join(model_ids))
    return header + content


def settings():
    '''Prints off the hardcoded "Magic Numbers" '''

    header = "Current Settings:\n-----------------------------------\n"
    body = "GPT3_MODEL:\t\t" + GPT3_MODEL + "\nGPT4_MODEL:\t\t" + GPT4_MODEL + "\nCODE_REVIEW_MODEL:\t" + CODE_REVIEW_MODEL + "\nIMG_MODEL:\t\t" + IMG_MODEL + "\nSIZE:\t\t\t" + SIZE + "\nSTYLE:\t\t\t" + STYLE + "\nVISION_MODEL:\t\t" + VISION_MODEL + "\nWHISPER_MODEL:\t\t" + WHISPER_MODEL + \
        "\nTTS_MODEL:\t\t" + TTS_MODEL + "\nTTS_VOICE:\t\t" + TTS_VOICE + "\nTUTOR_TEMP:\t\t" + str(TUTOR_TEMP) + \
        "\nCHAT_TEMP:\t\t" + str(CHAT_TEMP) + "\nFREQ_PENALTY:\t\t" + \
        str(FREQ_PENALTY) + "\nMAX_TOKENS:\t\t" + str(MAX_TOKENS)
    content = header + body
    return content


# Window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()
        self.default_font_norm = QFont(FONT, FONT_SIZE)
        app.setFont(self.default_font_norm)
        self.default_font_bold = QFont(FONT, FONT_SIZE)
        self.default_font_bold.setBold(True)
        self.setGeometry(100, 50, 900, 500)
        self.setWindowTitle("AI Assitant")
        self.clipboard = QApplication.clipboard()

        # Create a layout
        self.grid = QGridLayout()

        # Create frames
        self.radioframe = QFrame(self)
        self.buttonframe = QFrame(self)
        self.mainframe = QFrame(self)

        # Add frames to the layout
        self.grid.addWidget(self.radioframe, 0, 0)
        self.grid.addWidget(self.buttonframe, 1, 0)
        self.grid.addWidget(self.mainframe, 0, 1, 2, 1)

        # Radio button widgets
        self.vLayout1 = QVBoxLayout()
        radio_buttons = ["Chat 3.5", "Chat 4.0", "Tutor 3.5", "Tutor 4.0",
                         "Code Review", "Image Gen", "Vision", "Speech-to-Text", "Text-to-Speech", "List GPT Models", "List All Models", "List Settings"]
        for i, label in enumerate(radio_buttons, start=1):
            setattr(self, f'rb{i}', QRadioButton(label))
            self.vLayout1.addWidget(getattr(self, f'rb{i}'))
        self.rb2.setChecked(True)
        self.radioframe.setLayout(self.vLayout1)

        # Push button widgets
        self.vLayout2 = QVBoxLayout()
        self.cancel_btn = QPushButton("Clear")
        self.cancel_btn.setFixedWidth(BTN_WIDTH)
        self.help_btn = QPushButton("Help")
        self.help_btn.setFixedWidth(BTN_WIDTH)
        self.quit_btn = QPushButton("Quit")
        self.quit_btn.setFixedWidth(BTN_WIDTH)
        self.enter_btn = QPushButton("Enter")
        self.enter_btn.setFixedWidth(BTN_WIDTH)
        self.vLayout2.addWidget(self.cancel_btn)
        self.vLayout2.addWidget(self.help_btn)
        self.vLayout2.addWidget(self.quit_btn)
        self.vLayout2.addWidget(self.enter_btn)
        self.buttonframe.setLayout(self.vLayout2)

        self.cancel_btn.clicked.connect(self.on_cancel_click)
        self.help_btn.clicked.connect(self.on_help_click)
        self.quit_btn.clicked.connect(self.on_quit_click)
        self.enter_btn.clicked.connect(self.on_enter_click)

        # Text box widgets
        self.vLayout3 = QVBoxLayout()
        self.tutor_lbl = QLabel("Tutor:")
        self.tutor_lbl.setFont(self.default_font_bold)
        self.tutor_input = QTextEdit()
        self.tutor_input.setFixedHeight(TUTOR_INPUT_HT)
        self.user_lbl = QLabel("User:")
        self.user_lbl.setFont(self.default_font_bold)
        self.user_input = QTextEdit()
        self.user_input.setFixedHeight(USER_INPUT_HT)
        self.asst_lbl = QLabel("Assistant:")
        self.asst_lbl.setFont(self.default_font_bold)
        self.asst_resp = QTextEdit()
        self.asst_resp.setReadOnly(True)
        self.asst_resp.setFixedHeight(ASST_RESP_HT)
        self.vLayout3.addWidget(self.tutor_lbl)
        self.vLayout3.addWidget(self.tutor_input)
        self.vLayout3.addWidget(self.user_lbl)
        self.vLayout3.addWidget(self.user_input)
        self.vLayout3.addWidget(self.asst_lbl)
        self.vLayout3.addWidget(self.asst_resp)
        self.mainframe.setLayout(self.vLayout3)

        self.user_input.setFocus()
        self.setLayout(self.grid)
        self.show()

    def on_cancel_click(self):
        '''Clear all text boxes and reset radio button'''

        self.user_input.clear()
        self.tutor_input.clear()
        self.asst_resp.clear()
        self.rb2.setChecked(True)
        self.user_input.setFocus()

    def on_quit_click(self):
        '''Exit program'''

        sys.exit()

    def on_help_click(self):
        '''Displays Help text'''

        content = help_text()
        self.asst_resp.setPlainText(content)
        self.clipboard.setText(content)

    def no_prompt_user(self):
        '''Error message when no prompt detected'''

        self.asst_resp.setPlainText("Please enter a prompt in the 'User:' box")
        self.enter_btn.setEnabled(True)
        return

    def get_file_name(self):
        ''' Gets a file name to pass along to one of the openAI functions '''

        file = QFileDialog.getOpenFileName(None, "Select a File")
        return "" if file == "" else file[0]

    def on_enter_click(self):
        ''' Execute function associated with selected radio button'''

        self.enter_btn.setEnabled(False)
        self.text = self.user_input.toPlainText()
        if (self.rb1.isChecked() or self.rb2.isChecked()):
            if self.text == "":
                self.no_prompt_user()
                return
            if (self.rb1.isChecked()):
                chat_model = GPT3_MODEL
            else:
                chat_model = GPT4_MODEL
            content = chat(self.client, chat_model,
                           CHAT_TEMP, FREQ_PENALTY, 1, self.text, "")
        elif (self.rb3.isChecked() or self.rb4.isChecked()):
            tutor = self.tutor_input.toPlainText()
            if self.text == "":
                self.no_prompt_user()
                return
            if tutor == "":
                self.asst_resp.setPlainText(
                    "Please enter a subject area in the 'Tutor:' box")
                self.enter_btn.setEnabled(True)
                return
            if (self.rb3.isChecked()):
                chat_model = GPT3_MODEL
            else:
                chat_model = GPT4_MODEL
            content = chat(self.client, chat_model,
                           TUTOR_TEMP, FREQ_PENALTY, 0, self.text, tutor)
        elif self.rb5.isChecked():
            review_choice = self.get_file_name()
            content = code_reviewer(
                self.client, CODE_REVIEW_MODEL, review_choice)
        elif self.rb6.isChecked():
            if self.text == "":
                self.no_prompt_user()
                return
            url = image(self.client, IMG_MODEL, SIZE, STYLE, self.text)
            content = f"<a href='{url}'>{url}</a>"
        elif self.rb7.isChecked():
            img_path = self.get_file_name()
            content = vision(api_key, VISION_MODEL, MAX_TOKENS, img_path)
        elif self.rb8.isChecked():
            whisper_choice = self.get_file_name()
            content = whisper(self.client, WHISPER_MODEL, whisper_choice)
        elif (self.rb9.isChecked()):
            if self.text == "":
                self.no_prompt_user()
                return
            content = tts(self.client, TTS_MODEL, TTS_VOICE, self.text)
        elif (self.rb10.isChecked()):
            content = get_model_names(self.client, 1)
        elif (self.rb11.isChecked()):
            content = get_model_names(self.client, 0)
        elif (self.rb12.isChecked()):
            content = settings()
        if self.rb6.isChecked():
            self.asst_resp.setHtml(content)
            self.clipboard.setText(url)
            self.enter_btn.setEnabled(True)
            return
        else:
            self.asst_resp.setPlainText(content)
        self.clipboard.setText(content)
        self.user_input.clear()
        self.enter_btn.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
