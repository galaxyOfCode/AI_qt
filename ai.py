from os import getenv
import sys

from openai import OpenAI
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout)

from handlers import (get_model_names, get_settings, handle_chat,
                      handle_code_review, handle_image, handle_tts, handle_vision, handle_whisper)
from ui_components import MainFrame, ButtonFrame, RadioFrame

DEFAULT_FONT = QFont("Arial", 14)

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
        self.mainframe.user_input.setFocus()
        self.setLayout(self.grid)
        self.show()

    def no_user_prompt(self) -> None:
        """Error message when no user prompt detected"""
        self.mainframe.asst_resp.setPlainText(
            "Please enter a prompt in the 'User:' box")
        self.buttonframe.enter_btn.setEnabled(True)

    def no_tutor_prompt(self) -> None:
        """Error message when no tutor prompt detected"""
        self.mainframe.asst_resp.setPlainText(
            "Please enter a prompt in the 'Tutor:' box")
        self.buttonframe.enter_btn.setEnabled(True)

    def is_user_input_required(self) -> bool:
        """ Is text field required for the selected radio button"""
        checked_buttons = ["rb1", "rb2", "rb3", "rb4", "rb6", "rb9"]
        rb = self.radioframe.get_checked_button()
        return rb in checked_buttons

    def is_tutor_input_required(self) -> bool:
        """ Is text field required for the selected radio button"""
        rb = self.radioframe.get_checked_button()
        return rb == "rb3" or rb == "rb4"

    def set_response(self, content) -> None:
        """Implement setting the response in the UI"""
        rb = self.radioframe.get_checked_button()
        if rb == "rb6":
            self.mainframe.asst_resp.setHtml(
                f"<a href='{content}'>{content}</a>")
        else:
            self.mainframe.asst_resp.clear()
            self.mainframe.asst_resp.setPlainText(content)

    def on_enter_click(self) -> None:
        """Execute function associated with selected radio button"""
        self.buttonframe.enter_btn.setEnabled(False)
        text = self.mainframe.user_input.toPlainText()
        tutor = self.mainframe.tutor_input.toPlainText()

        if not text and self.is_user_input_required():
            self.no_user_prompt()
            return

        if not tutor and self.is_tutor_input_required():
            self.no_tutor_prompt()
            return

        action_mapping = {
            self.radioframe.rb1: lambda: handle_chat(self.client, 1, 1, text, ""),
            self.radioframe.rb2: lambda: handle_chat(self.client, 2, 1, text, ""),
            self.radioframe.rb3: lambda: handle_chat(self.client, 3, 0, text, tutor),
            self.radioframe.rb4: lambda: handle_chat(self.client, 4, 0, text, tutor),
            self.radioframe.rb5: lambda: handle_code_review(self.client),
            self.radioframe.rb6: lambda: handle_image(self.client, text),
            self.radioframe.rb7: lambda: handle_vision(api_key),
            self.radioframe.rb8: lambda: handle_whisper(self.client),
            self.radioframe.rb9: lambda: handle_tts(self.client, text),
            self.radioframe.rb10: lambda: get_model_names(self.client, 1),
            self.radioframe.rb11: lambda: get_model_names(self.client, 0),
            self.radioframe.rb12: lambda: get_settings(),
        }

        for rb, action in action_mapping.items():
            if rb.isChecked():
                content = action()
                break

        self.set_response(content)
        self.clipboard.setText(content)
        self.buttonframe.enter_btn.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
