from PyQt6.QtWidgets import QFrame, QVBoxLayout, QRadioButton


class RadioFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.radio_buttons = []
        radio_button_labels = ["Chat 3.5", "Chat 4.0", "Tutor 3.5", "Tutor 4.0",
                         "Code Review", "Image Gen", "Vision", "Speech-to-Text",
                         "Text-to-Speech", "List GPT Models", "List All Models", "List Settings"]
        for label in enumerate(radio_button_labels, start=1):
            rb = QRadioButton(label)
            self.radio_buttons.append(rb)
            self.layout.addWidget(rb)
        self.rb2.setChecked(True)
        self.setLayout(self.layout)

    def get_checked_radio_button(self):
        for rb in self.radio_buttons:
            if rb.isChecked():
                print(rb.text)
                return rb.text()
        return None
