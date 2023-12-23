import os
import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *

from openai import OpenAI
from chat import chat
from code_review import code_reviewer
from image import vision, image
from voice import tts, whisper
from help import help_text

client = OpenAI()

VERSION = "1.3"
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

rb1, rb2, rb3, rb4, rb5, rb6, rb7, rb8, rb9, rb10, rb11, rb12 = [None] * 12
user_input, asst_resp, tutor_input = None, None, None
enter_btn, cancel_btn, quit_btn, clipboard = None, None, None, None

api_key = os.environ.get("OPENAI_API_KEY")


def list_gpt_models(client):
    '''List only the GPT models available through the API'''

    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    gpt_model_ids = [
        model_id for model_id in model_ids if model_id.startswith("gpt")]
    gpt_model_ids.sort()
    header = "Current GPT Models\n------------------\n"
    content = ("\n".join(gpt_model_ids))
    return header + content


def list_models(client):
    ''' List ALL openAI models available through the API '''

    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    model_ids.sort()
    header = "Current openAI Models\n---------------------\n"
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


def on_cancel_click():
    '''Clear all text boxes and reset radio button'''

    user_input.clear()
    tutor_input.clear()
    asst_resp.clear()
    rb2.setChecked(True)
    user_input.setFocus()


def on_help_click():
    content = help_text()
    asst_resp.setPlainText(content)


def on_enter_click():
    ''' Execute function associated with selected radio button'''

    enter_btn.setEnabled(False)
    text = user_input.toPlainText()
    if (rb1.isChecked() or rb2.isChecked()):
        if (rb1.isChecked()):
            chat_model = GPT3_MODEL
        else:
            chat_model = GPT4_MODEL
        content = chat(client, chat_model,
                       CHAT_TEMP, FREQ_PENALTY, 1, text, "")
    elif (rb3.isChecked() or rb4.isChecked()):
        tutor = tutor_input.toPlainText()
        if (rb3.isChecked()):
            chat_model = GPT3_MODEL
        else:
            chat_model = GPT4_MODEL
        content = chat(client, chat_model,
                       TUTOR_TEMP, FREQ_PENALTY, 0, text, tutor)
    elif rb5.isChecked():
        review_choice = QFileDialog.getOpenFileName(None, "Select a File")
        content = code_reviewer(client, CODE_REVIEW_MODEL, review_choice[0])
    elif rb6.isChecked():
        url = image(client, IMG_MODEL, SIZE, STYLE, text)
        content = f"<a href='{url}'>{url}</a>"
    elif rb7.isChecked():
        img_path = QFileDialog.getOpenFileName(None, "Select a File")
        content = vision(api_key, VISION_MODEL, MAX_TOKENS, img_path[0])
    elif rb8.isChecked():
        whisper_choice = QFileDialog.getOpenFileName(None, "Select a File")
        content = whisper(client, WHISPER_MODEL, whisper_choice[0])
    elif (rb9.isChecked()):
        content = tts(client, TTS_MODEL, TTS_VOICE, text)
    elif (rb10.isChecked()):
        content = list_gpt_models(client)
    elif (rb11.isChecked()):
        content = list_models(client)
    elif (rb12.isChecked()):
        content = settings()
    if rb6.isChecked():
        asst_resp.setHtml(content)
    else:
        asst_resp.setPlainText(content)
    clipboard.setText(content)
    user_input.clear()
    enter_btn.setEnabled(True)


def on_quit_click():
    '''Exit program'''

    sys.exit()


# Window
def window():
    ''' Main program '''

    global rb1, rb2, rb3, rb4, rb5, rb6, rb7, rb8, rb9, rb10, rb11, rb12, user_input, asst_resp, tutor_input, cancel_btn, quit_btn, enter_btn, clipboard
    app = QApplication(sys.argv)
    clipboard = QApplication.clipboard()
    default_font_norm = QFont(FONT, FONT_SIZE)
    app.setFont(default_font_norm)
    default_font_bold = QFont(FONT, FONT_SIZE)
    default_font_bold.setBold(True)

    main_window = QWidget()
    main_window.setGeometry(100, 50, 900, 500)
    main_window.setWindowTitle(f"AI Assitant")

    # Create a layout
    grid = QGridLayout()

    # Create frames
    radioframe = QFrame(main_window)
    buttonframe = QFrame(main_window)
    mainframe = QFrame(main_window)

    # Add frames to the layout
    grid.addWidget(radioframe, 0, 0)
    grid.addWidget(buttonframe, 1, 0)
    grid.addWidget(mainframe, 0, 1, 2, 1)

    # Radio button widgets
    vLayout1 = QVBoxLayout()
    rb1 = QRadioButton("Chat 3.5")
    rb2 = QRadioButton("Chat 4.0")
    rb2.setChecked(True)
    rb3 = QRadioButton("Tutor 3.5")
    rb4 = QRadioButton("Tutor 4.0")
    rb5 = QRadioButton("Code Review")
    rb6 = QRadioButton("Image Gen")
    rb7 = QRadioButton("Vision")
    rb8 = QRadioButton("Speech-to-Text")
    rb9 = QRadioButton("Text-to-Speech")
    rb10 = QRadioButton("List GPT")
    rb11 = QRadioButton("List All")
    rb12 = QRadioButton("List Settings")
    vLayout1.addWidget(rb1)
    vLayout1.addWidget(rb2)
    vLayout1.addWidget(rb3)
    vLayout1.addWidget(rb4)
    vLayout1.addWidget(rb5)
    vLayout1.addWidget(rb6)
    vLayout1.addWidget(rb7)
    vLayout1.addWidget(rb8)
    vLayout1.addWidget(rb9)
    vLayout1.addWidget(rb10)
    vLayout1.addWidget(rb11)
    vLayout1.addWidget(rb12)
    radioframe.setLayout(vLayout1)

    # Push button widgets
    vLayout2 = QVBoxLayout()
    cancel_btn = QPushButton("Clear")
    cancel_btn.setFixedWidth(BTN_WIDTH)
    help_btn = QPushButton("Help")
    help_btn.setFixedWidth(BTN_WIDTH)
    quit_btn = QPushButton("Quit")
    quit_btn.setFixedWidth(BTN_WIDTH)
    enter_btn = QPushButton("Enter")
    enter_btn.setFixedWidth(BTN_WIDTH)
    vLayout2.addWidget(cancel_btn)
    vLayout2.addWidget(help_btn)
    vLayout2.addWidget(quit_btn)
    vLayout2.addWidget(enter_btn)
    buttonframe.setLayout(vLayout2)
    cancel_btn.clicked.connect(on_cancel_click)
    help_btn.clicked.connect(on_help_click)
    quit_btn.clicked.connect(on_quit_click)
    enter_btn.clicked.connect(on_enter_click)

    # Text box widgets
    vLayout3 = QVBoxLayout()
    tutor_lbl = QLabel("Tutor:")
    tutor_lbl.setFont(default_font_bold)
    tutor_input = QTextEdit()
    tutor_input.setFixedHeight(TUTOR_INPUT_HT)
    user_lbl = QLabel("You:")
    user_lbl.setFont(default_font_bold)
    user_input = QTextEdit()
    user_input.setFixedHeight(USER_INPUT_HT)
    asst_lbl = QLabel("Assistant:")
    asst_lbl.setFont(default_font_bold)
    asst_resp = QTextEdit()
    asst_resp.setReadOnly(True)
    asst_resp.setFixedHeight(ASST_RESP_HT)
    vLayout3.addWidget(tutor_lbl)
    vLayout3.addWidget(tutor_input)
    vLayout3.addWidget(user_lbl)
    vLayout3.addWidget(user_input)
    vLayout3.addWidget(asst_lbl)
    vLayout3.addWidget(asst_resp)
    mainframe.setLayout(vLayout3)

    user_input.setFocus()
    main_window.setLayout(grid)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    window()
