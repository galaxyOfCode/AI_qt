from PyQt6.QtWidgets import (
    QTextEdit, QFrame, QVBoxLayout, QRadioButton, QPushButton, QLabel)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QCoreApplication
from help import help_text

BTN_WIDTH = 80
TUTOR_INPUT_HT = 30
USER_INPUT_HT = 100
ASST_RESP_HT = 300
ASST_FONT = QFont("Menlo", 13)
DEFAULT_FONT = QFont("Arial", 14)

class RadioFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.vLayout1 = QVBoxLayout()
        radio_buttons = ["Chat 3.5", "Chat 4.0", "Tutor 3.5", "Tutor 4.0",
                         "Code Review", "Image Gen", "Vision", "Speech-to-Text",
                         "Text-to-Speech", "List GPT Models", "List All Models", "List Settings"]
        self.radio_buttons_count = len(radio_buttons)
        for i, label in enumerate(radio_buttons, start=1):
            setattr(self, f'rb{i}', QRadioButton(label))
            self.vLayout1.addWidget(getattr(self, f'rb{i}'))
        self.rb2.setChecked(True)
        self.setLayout(self.vLayout1)

    def get_checked_button(self):
        for i in range(1, self.radio_buttons_count + 1):
            rb = getattr(self, f'rb{i}')
            if rb.isChecked():
                return f'rb{i}'
        return None


class ButtonFrame(QFrame):
    def __init__(self, mainframe, parent=None):
        super().__init__(parent)
        self.mainframe = mainframe
        self.init_ui()
        self.connect()

    def init_ui(self):
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
        self.setLayout(self.vLayout2)

    def connect(self):
        self.quit_btn.clicked.connect(self.on_quit_click)
        self.cancel_btn.clicked.connect(self.mainframe.on_cancel_click)
        self.help_btn.clicked.connect(self.mainframe.on_help_click)

    def on_quit_click(self) -> None:
        """ Exit program """
        QCoreApplication.quit()

class MainFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_font_bold = DEFAULT_FONT
        self.default_font_bold.setBold(True)
        self.init_ui()

    def init_ui(self):
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
        self.asst_resp.setFont(ASST_FONT)
        self.asst_resp.setFixedHeight(ASST_RESP_HT)
        self.vLayout3.addWidget(self.tutor_lbl)
        self.vLayout3.addWidget(self.tutor_input)
        self.vLayout3.addWidget(self.user_lbl)
        self.vLayout3.addWidget(self.user_input)
        self.vLayout3.addWidget(self.asst_lbl)
        self.vLayout3.addWidget(self.asst_resp)
        self.setLayout(self.vLayout3)

    def on_cancel_click(self) -> None:
        """ Clear all text boxes and reset radio button """
        self.user_input.clear()
        self.tutor_input.clear()
        self.asst_resp.clear()
        self.user_input.setFocus()

    def on_help_click(self) -> None:
        """Displays Help text"""
        content = help_text()
        self.asst_resp.setPlainText(content)
