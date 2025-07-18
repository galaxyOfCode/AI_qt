import logging
from PyQt6.QtWidgets import (QTextEdit, QFrame, QVBoxLayout,
                             QRadioButton, QPushButton, QLabel,
                             QFileDialog, QHBoxLayout, QComboBox)
from PyQt6.QtCore import QCoreApplication, Qt

from config import Config

config = Config()


# Set up basic logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbosity
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class RadioFrame(QFrame):
    """This class creates a frame with radio buttons for different functions.
    It allows the user to select a function for the AI assistant to perform."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.radio_layout = QVBoxLayout(self)
        self.radio_buttons = []  # List to store radio buttons
        self.radio_button_labels = ["Chat", "Code Review", "Image Gen", "Vision", 
                                    "Speech-to-Text", "Text-to-Speech", "List All Models", 
                                    "Update API", "List Settings"]
        self.add_widgets()
        self.layout_ui()

    def layout_ui(self) -> None:
        self.radio_buttons[0].setChecked(True)
        self.setLayout(self.radio_layout)

    def add_widgets(self) -> None:
        for label in self.radio_button_labels:
            rb = QRadioButton(label)
            self.radio_buttons.append(rb)
            self.radio_layout.addWidget(rb)

    def get_checked_radio_button(self) -> str | None:
        for rb in self.radio_buttons:
            if rb.isChecked():
                return rb.text()
        return None


class ModelFrame(QFrame):
    """This class creates a frame with a combo box for selecting different AI models.
    It allows the user to choose a model for the AI assistant."""

    def __init__(self, parent=None, models=None) -> None:
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        # Label
        self.label = QLabel("Model:")
        self.label.setFixedWidth(50)

        # Combo box
        self.combo = QComboBox()
        models = config.MODEL_LIST 
        for m in models:
            self.combo.addItem(m)

        # Assemble
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.setLayout(self.layout)

    def get_selected_model(self) -> str:
        return self.combo.currentText()
    

class ReasonFrame(QFrame):
    """This class creates a frame with radio buttons for selecting the reasoning or image quality level. It allows the user to choose the level of reasoning or image quality for the AI assistant."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self.radio_buttons = []
        self.radio_button_labels = ["low", "medium", "high"]
        
        self.label = QLabel("Reasoning/Image Quality:")

        # Create the vertical layout for the label + buttons
        self.main_layout = QVBoxLayout(self)
        
        # Create a horizontal layout just for the radio buttons
        self.button_layout = QHBoxLayout()
        
        self.add_widgets()
        self.layout_ui()

    def layout_ui(self) -> None:
        self.radio_buttons[1].setChecked(True)
        self.setLayout(self.main_layout)

    def add_widgets(self) -> None:
        self.main_layout.addWidget(self.label)
        for label in self.radio_button_labels:
            rb = QRadioButton(label)
            self.radio_buttons.append(rb)
            self.button_layout.addWidget(rb)
        self.main_layout.addLayout(self.button_layout)

    def get_checked_radio_button(self) -> str | None:
        for rb in self.radio_buttons:
            if rb.isChecked():
                return rb.text()
        return None
    

# noinspection PyUnresolvedReferences
class ButtonFrame(QFrame):
    """This class creates a frame with buttons for various actions such as About, Clear, Help, Quit, Save, and Enter."""

    def __init__(self, mainframe, parent=None) -> None:
        super().__init__(parent)
        self.mainframe = mainframe
        self.button_layout = QVBoxLayout()
        self.about_btn = QPushButton("About")
        self.clear_btn = QPushButton("Clear")
        self.help_btn = QPushButton("Help")
        self.quit_btn = QPushButton("Quit")
        self.save_btn = QPushButton("Save")
        self.enter_btn = QPushButton("Enter")
        self.set_ui_properties()
        self.layout_ui()
        self.setup_connections()

    def set_ui_properties(self) -> None:
        self.about_btn.setFixedWidth(config.BTN_WIDTH)
        self.clear_btn.setFixedWidth(config.BTN_WIDTH)
        self.enter_btn.setFixedWidth(config.BTN_WIDTH)
        self.quit_btn.setFixedWidth(config.BTN_WIDTH)
        self.save_btn.setFixedWidth(config.BTN_WIDTH)
        self.help_btn.setFixedWidth(config.BTN_WIDTH)

    def layout_ui(self) -> None:
        self.button_layout.addWidget(self.enter_btn)
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.clear_btn)
        self.button_layout.addWidget(self.about_btn)
        self.button_layout.addWidget(self.help_btn)
        self.button_layout.addWidget(self.quit_btn)
        self.setLayout(self.button_layout)

    def setup_connections(self) -> None:
        self.quit_btn.clicked.connect(self.on_quit_click)
        self.about_btn.clicked.connect(self.mainframe.on_about_click)
        self.clear_btn.clicked.connect(self.mainframe.on_clear_click)
        self.help_btn.clicked.connect(self.mainframe.on_help_click)
        self.save_btn.clicked.connect(self.mainframe.on_save_click)

    def on_quit_click(self) -> None:
        """ Exit program """
        logger.info("Quit button clicked")
        QCoreApplication.quit()


class MainFrame(QFrame):
    """This class creates the main frame for the AI assistant application.
    It includes user input and assistant response text areas, along with buttons for various actions."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.default_font_bold = config.DEFAULT_FONT
        self.default_font_bold.setBold(True)
        self.main_layout = QVBoxLayout()
        self.user_lbl = QLabel("User:")
        self.user_input = QTextEdit()
        self.asst_lbl = QLabel("Assistant:")
        self.asst_resp = QTextEdit()
        self.set_ui_properties()
        self.add_widgets()

    def set_ui_properties(self) -> None:
        self.user_lbl.setFont(self.default_font_bold)
        self.user_input.setFixedHeight(config.USER_INPUT_HT)
        self.asst_lbl.setFont(self.default_font_bold)
        self.asst_resp.setReadOnly(True)
        self.asst_resp.setFont(config.ASST_FONT)
        self.asst_resp.setFixedHeight(config.ASST_RESP_HT)
        self.user_input.setFocus()

    def add_widgets(self) -> None:
        self.main_layout.addWidget(self.user_lbl)
        self.main_layout.addWidget(self.user_input)
        self.main_layout.addWidget(self.asst_lbl)
        self.main_layout.addWidget(self.asst_resp)
        self.setLayout(self.main_layout)

    def on_clear_click(self) -> None:
        """ Clear all text boxes and reset radio button """

        self.user_input.clear()
        self.asst_resp.clear()
        config.reload_config()
        self.asst_resp.setTextColor(Qt.GlobalColor.black)
        self.asst_resp.setFontUnderline(False)
        self.user_input.setFont(config.DEFAULT_FONT)
        self.user_input.setFocus()

    def on_help_click(self) -> None:
        """Displays Help text"""

        try:
            with open(config.help_file, "r") as file:
                content = file.read()
                logger.info("Help content returned")
            self.asst_resp.setPlainText(content)
        except FileNotFoundError:
            logger.exception("This is an exception trace.", exc_info=True)
            self.asst_resp.setPlainText("Help file not found.")

    def on_about_click(self) -> None:
        """Displays About text (Version Number)"""

        about_content = "AI Assistant created by Jeff Hall"
        self.user_input.clear()
        self.asst_resp.clear()
        logger.info("About content returned")
        self.asst_resp.setPlainText(f"{about_content}\n{config.version}")

    def on_save_click(self) -> None:
        file_name, _ = QFileDialog.getSaveFileName(
            None,
            "Save File",
            config.clipboard_path,
            "Text files (*.txt)",)
        if file_name:
            with open(file_name, "w") as file:
                file.write(self.asst_resp.toPlainText())
            logger.info("File saved successfully")
            self.asst_resp.setPlainText(f"{file_name} succesfully created")
        else:
            self.asst_resp.setPlainText("No file selected.")
            logger.info("No file selected for saving.")
