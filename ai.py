from openai import OpenAI
from PyQt6.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QFileDialog)

from chat import chat
from config import Config
from frames import MainFrame, ButtonFrame, RadioFrame, ModelFrame, ReasonFrame
from image import describe_image, generate_image
from reviewer import code_review
from utilities import get_model_names, get_settings, update
from voice import text_to_speech, speech_to_text

config = Config()


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
        self.default_font_norm = config.DEFAULT_FONT
        self.setFont(self.default_font_norm)
        self.default_font_bold = config.DEFAULT_FONT
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
        self.modelframe = ModelFrame(self.mainframe)
        self.reasonframe = ReasonFrame(self.mainframe)

        # Add frames to the layout
        self.grid.addWidget(self.radioframe, 0, 0)
        self.grid.addWidget(self.modelframe, 1, 0)
        self.grid.addWidget(self.reasonframe, 2, 0)
        self.grid.addWidget(self.buttonframe, 3, 0)
        self.grid.addWidget(self.mainframe, 0, 1, 4, 1)

        # Set Enter button action
        self.buttonframe.enter_btn.clicked.connect(self.on_enter_click)

        # Set layout
        self.setLayout(self.grid)
        self.mainframe.user_input.setFocus()

    def no_prompt(self, box) -> None:
        """Error message when no required user prompt detected"""

        self.mainframe.asst_resp.setPlainText(
            f"Please enter a prompt in the '{box}:' box")
        self.buttonframe.enter_btn.setEnabled(True)

    def is_user_input_required(self) -> bool:
        """ Is a text field required for the selected radio button"""

        checked_buttons = ["Chat", "Image Gen", "Text-to-Speech",
                           "Vision"]
        button = self.radioframe.get_checked_radio_button()
        return button in checked_buttons

    @staticmethod
    def get_file_name() -> str:
        """ Gets a file name to pass along to one of the openAI functions """

        file = QFileDialog.getOpenFileName(None, "Select a File")
        return "" if file == "" else file[0]

    def set_response(self, content) -> None:
        """Implement setting the response in the UI"""

        button = self.radioframe.get_checked_radio_button()
        if button == "Image Gen":
            self.mainframe.asst_resp.setHtml(
                f"<a href='{content}'>{content}</a>")
        else:
            self.mainframe.asst_resp.clear()
            self.mainframe.asst_resp.setPlainText(content)

    def on_enter_click(self) -> None:
        """Execute function associated with selected radio button"""

        content = ""
        self.mainframe.asst_resp.setPlainText("Processing . . .")
        self.buttonframe.enter_btn.setEnabled(False)
        user_text = self.mainframe.user_input.toPlainText()
        chosen_model = self.modelframe.combo.currentText()
        if chosen_model.startswith("gpt") or chosen_model == "o1-mini":
            r_flag = 0
        else:
            r_flag = 1 
        
        reasoning = self.reasonframe.get_checked_radio_button()

        if not user_text and self.is_user_input_required():
            self.no_prompt("User")
            return
        
        action_mapping = {
            self.radioframe.radio_buttons[0]: lambda: chat(self.client,
                                                           chosen_model, 
                                                           reasoning,
                                                           user_text, 
                                                           r_flag),
            self.radioframe.radio_buttons[1]: lambda: code_review(self.client,
                                                                  chosen_model,
                                                                  self.get_file_name()),
            self.radioframe.radio_buttons[2]: lambda: generate_image(self.client,
                                                                     config.IMG_MODEL,
                                                                     reasoning, user_text,
                                                                     config.IMG_SIZE,
                                                                     config.image_path),
            self.radioframe.radio_buttons[3]: lambda: describe_image(config.api_key,
                                                                     chosen_model,
                                                                     config.MAX_TOKENS, self.get_file_name(), user_text),
            self.radioframe.radio_buttons[4]: lambda: speech_to_text(self.client,
                                                                     config.WHISPER_MODEL,
                                                                     self.get_file_name()),
            self.radioframe.radio_buttons[5]: lambda: text_to_speech(self.client,
                                                                     config.TTS_MODEL,
                                                                     config.TTS_VOICE, user_text,
                                                                     config.speech_file_path),
            self.radioframe.radio_buttons[6]: lambda: get_model_names(self.client),
            self.radioframe.radio_buttons[7]: lambda: update(),
            self.radioframe.radio_buttons[8]: lambda: get_settings(config),
        }

        for button, action in action_mapping.items():
            if button.isChecked():
                content = action()
                break

        self.set_response(content)
        self.clipboard.setText(content)
        self.buttonframe.enter_btn.setEnabled(True)


def main() -> None:
    app = QApplication([])
    mw = MainWindow()
    mw.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
