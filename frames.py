from PyQt6.QtWidgets import (
    QTextEdit, QFrame, QVBoxLayout, QRadioButton, QPushButton, QLabel)
from PyQt6.QtCore import QCoreApplication
from config import Config

config = Config()


class RadioFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.add_widgets()
        self.layout_ui()

    def init_ui(self) -> None:
        self.radio_layout = QVBoxLayout(self)
        self.radio_buttons = []  # List to store radio buttons

        self.radio_button_labels = ["Chat 3.5", "Chat 4.0", "Tutor 3.5", "Tutor 4.0", "Code Review", "Image Gen",
                                    "Vision", "Speech-to-Text", "Text-to-Speech", "List GPT Models", "List All Models", "List Settings"]

    def add_widgets(self) -> None:
        for label in self.radio_button_labels:
            rb = QRadioButton(label)
            self.radio_buttons.append(rb)
            self.radio_layout.addWidget(rb)

    def layout_ui(self) -> None:
        self.radio_buttons[1].setChecked(True)
        self.setLayout(self.radio_layout)

    def get_checked_radio_button(self):
        for rb in self.radio_buttons:
            if rb.isChecked():
                return rb.text()
        return None


class ButtonFrame(QFrame):
    def __init__(self, mainframe, parent=None):
        super().__init__(parent)
        self.mainframe = mainframe
        self.init_ui()
        self.layout_ui()
        self.ui_properties()
        self.setup_connections()

    def init_ui(self) -> None:
        self.button_layout = QVBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.help_btn = QPushButton("Help")
        self.quit_btn = QPushButton("Quit")
        self.enter_btn = QPushButton("Enter")

    def ui_properties(self) -> None:
        self.clear_btn.setFixedWidth(config.BTN_WIDTH)
        self.enter_btn.setFixedWidth(config.BTN_WIDTH)
        self.quit_btn.setFixedWidth(config.BTN_WIDTH)
        self.help_btn.setFixedWidth(config.BTN_WIDTH)

    def layout_ui(self) -> None:
        self.button_layout.addWidget(self.clear_btn)
        self.button_layout.addWidget(self.help_btn)
        self.button_layout.addWidget(self.quit_btn)
        self.button_layout.addWidget(self.enter_btn)
        self.setLayout(self.button_layout)

    def setup_connections(self) -> None:
        self.quit_btn.clicked.connect(self.on_quit_click)
        self.clear_btn.clicked.connect(self.mainframe.on_clear_click)
        self.help_btn.clicked.connect(self.mainframe.on_help_click)

    def on_quit_click(self) -> None:
        """ Exit program """
        
        QCoreApplication.quit()


class MainFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_font_bold = config.DEFAULT_FONT
        self.default_font_bold.setBold(True)
        self.init_ui()
        self.ui_properties()
        self.add_widgets()

    def init_ui(self) -> None:
        self.main_layout = QVBoxLayout()
        self.tutor_lbl = QLabel("Tutor:")
        self.tutor_input = QTextEdit()
        self.user_lbl = QLabel("User:")
        self.user_input = QTextEdit()
        self.asst_lbl = QLabel("Assistant:")
        self.asst_resp = QTextEdit()

    def ui_properties(self) -> None:
        self.tutor_lbl.setFont(self.default_font_bold)
        self.tutor_input.setFixedHeight(config.TUTOR_INPUT_HT)
        self.user_lbl.setFont(self.default_font_bold)
        self.user_input.setFixedHeight(config.USER_INPUT_HT)
        self.asst_lbl.setFont(self.default_font_bold)
        self.asst_resp.setReadOnly(True)
        self.asst_resp.setFont(config.ASST_FONT)
        self.asst_resp.setFixedHeight(config.ASST_RESP_HT)
        self.user_input.setFocus()

    def add_widgets(self) -> None:
        self.main_layout.addWidget(self.tutor_lbl)
        self.main_layout.addWidget(self.tutor_input)
        self.main_layout.addWidget(self.user_lbl)
        self.main_layout.addWidget(self.user_input)
        self.main_layout.addWidget(self.asst_lbl)
        self.main_layout.addWidget(self.asst_resp)
        self.setLayout(self.main_layout)

    def on_clear_click(self) -> None:
        """ Clear all text boxes and reset radio button """
        self.user_input.clear()
        self.tutor_input.clear()
        self.asst_resp.clear()
        self.user_input.setFocus()

    def on_help_click(self) -> None:
        """Displays Help text"""
        with open('help.txt') as file:
            content = file.read()
            self.asst_resp.setPlainText(content)
