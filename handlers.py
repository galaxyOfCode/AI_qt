from PyQt6.QtWidgets import QFileDialog

from chat import chat
from code_review import code_reviewer
from image import vision, image
from voice import tts, whisper

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

def handle_chat(client, button, option, text, tutor) -> str:
    """Implement the chat functionality"""
    if button == 1 or button == 3:
        model = GPT3_MODEL
    else:
        model = GPT4_MODEL
    return chat(client, model, CHAT_TEMP, FREQ_PENALTY, option, text, tutor)

def handle_code_review(client) -> str:
    """Implement the code review functionality"""
    review_choice = get_file_name()
    return code_reviewer(client, GPT4_MODEL, review_choice)

def handle_image(client, text) -> str:
    """Implement the image generation functionality"""
    return image(client, IMG_MODEL, SIZE, STYLE, text)

def handle_vision(api_key) -> str:
    """Implement the vision functionality"""
    img_path = get_file_name()
    return vision(api_key, VISION_MODEL, MAX_TOKENS, img_path)

def handle_whisper(client) -> str:
    """Implement the speech-to-text functionality"""
    whisper_choice = get_file_name()
    return whisper(client, WHISPER_MODEL, whisper_choice)

def handle_tts(client, text) -> str:
    """Implement the text-to-speech functionality"""
    return tts(client, TTS_MODEL, TTS_VOICE, text)

def get_model_names(client, option) -> str:
    """List either the GPT models, or all models available through the API"""

    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    if option == 1:
        model_ids = [
            model_id for model_id in model_ids if model_id.startswith("gpt")]
        header = "Current openAI GPT Models:\n\n"
    else:
        header = "Current openAI Models:\n\n"
    model_ids.sort()
    content = ("\n".join(model_ids))
    return header + content


def get_settings() -> str:
    """ Print all hardcoded 'Magic Numbers' """
    settings = {
        "GPT3_MODEL:": GPT3_MODEL,
        "GPT4_MODEL:": GPT4_MODEL,
        "CODE_REVIEW_MODEL:": CODE_REVIEW_MODEL,
        "IMG_MODEL:": IMG_MODEL,
        "SIZE:": SIZE,
        "STYLE:": STYLE,
        "VISION_MODEL:": VISION_MODEL,
        "WHISPER_MODEL:": WHISPER_MODEL,
        "TTS_MODEL:": TTS_MODEL,
        "TTS_VOICE:": TTS_VOICE,
        "TUTOR_TEMP:": TUTOR_TEMP,
        "CHAT_TEMP:": CHAT_TEMP,
        "FREQ_PENALTY:": FREQ_PENALTY,
        "MAX_TOKENS:": MAX_TOKENS
    }
    longest_key_length = max(len(key) for key in settings)
    content = "Current Settings:\n\n"
    for key, value in settings.items():
        buffer = " " * (longest_key_length - len(key))
        content += f"{key}{buffer}\t{value}\n"
    return content


def get_file_name() -> str:
    """ Gets a file name to pass along to one of the openAI functions """

    file = QFileDialog.getOpenFileName(None, "Select a File")
    return "" if file == "" else file[0]