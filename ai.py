from os import getenv
import sys

from openai import OpenAI
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QFrame,
                             QVBoxLayout, QRadioButton, QPushButton, QLabel,
                             QTextEdit)

from help import help_text
from handlers import (get_model_names, get_settings, handle_chat,
                      handle_code_review, handle_image, handle_tts, handle_vision, handle_whisper)

BTN_WIDTH = 80
DEFAULT_FONT = QFont("Arial", 14)
ASST_FONT = QFont("Menlo", 13)
TUTOR_INPUT_HT = 30
USER_INPUT_HT = 100
ASST_RESP_HT = 300

api_key = getenv("OPENAI_API_KEY")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()
        self.default_font_norm = DEFAULT_FONT
        app.setFont(self.default_font_norm)
        self.default_font_bold = DEFAULT_FONT
        self.default_font_bold.setBold(True)
        self.setGeometry(100, 50, 900, 500)
        self.setWindowTitle("AI Assistant")
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
                         "Code Review", "Image Gen", "Vision", "Speech-to-Text",
                         "Text-to-Speech", "List GPT Models", "List All Models", "List Settings"]
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
        self.asst_resp.setFont(ASST_FONT)
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

    def on_cancel_click(self) -> None:
        """ Clear all text boxes and reset radio button """
        self.user_input.clear()
        self.tutor_input.clear()
        self.asst_resp.clear()
        self.rb2.setChecked(True)
        self.user_input.setFocus()

    def on_help_click(self) -> None:
        """Displays Help text"""
        content = help_text()
        self.asst_resp.setPlainText(content)
        self.clipboard.setText(content)

    def on_quit_click(self) -> None:
        """ Exit program """
        QCoreApplication.quit()

    def no_prompt_user(self) -> None:
        """Error message when no user prompt detected"""
        self.asst_resp.setPlainText("Please enter a prompt in the 'User:' box")
        self.enter_btn.setEnabled(True)

    def no_prompt_tutor(self) -> None:
        """Error message when no tutor prompt detected"""
        self.asst_resp.setPlainText(
            "Please enter a prompt in the 'Tutor:' box")
        self.enter_btn.setEnabled(True)

    def is_user_input_required(self) -> bool:
        """ Is text field required for the selected radio button"""
        return self.rb1.isChecked() or self.rb2.isChecked() or self.rb3.isChecked() or self.rb4.isChecked() or self.rb6.isChecked() or self.rb9.isChecked()

    def is_tutor_input_required(self) -> bool:
        """ Is text field required for the selected radio button"""
        return self.rb3.isChecked() or self.rb4.isChecked()

    def set_response(self, content) -> None:
        """Implement setting the response in the UI"""
        if self.rb6.isChecked():
            self.asst_resp.setHtml(f"<a href='{content}'>{content}</a>")
        else:
            self.asst_resp.clear()
            self.asst_resp.setPlainText(content)

    def on_enter_click(self) -> None:
        """Execute function associated with selected radio button"""
        self.enter_btn.setEnabled(False)
        text = self.user_input.toPlainText()
        tutor = self.tutor_input.toPlainText()

        if not text and self.is_user_input_required():
            self.no_prompt_user()
            return

        if not tutor and self.is_tutor_input_required():
            self.no_prompt_tutor()
            return

        action_mapping = {
            self.rb1: lambda: handle_chat(self.client, 1, 1, text, ""),
            self.rb2: lambda: handle_chat(self.client, 2, 1, text, ""),
            self.rb3: lambda: handle_chat(self.client, 3, 0, text, tutor),
            self.rb4: lambda: handle_chat(self.client, 4, 0, text, tutor),
            self.rb5: lambda: handle_code_review(self.client),
            self.rb6: lambda: handle_image(self.client, text),
            self.rb7: lambda: handle_vision(api_key),
            self.rb8: lambda: handle_whisper(self.client),
            self.rb9: lambda: handle_tts(self.client, text),
            self.rb10: lambda: get_model_names(self.client, 1),
            self.rb11: lambda: get_model_names(self.client, 0),
            self.rb12: lambda: get_settings(),
        }

        for rb, action in action_mapping.items():
            if rb.isChecked():
                content = action()
                break

        self.set_response(content)
        self.clipboard.setText(content)
        self.enter_btn.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
