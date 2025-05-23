import logging
import openai
from PyQt6.QtWidgets import QFileDialog

from errors import handle_file_errors, handle_openai_errors

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


def speech_to_text(client, model, choice) -> str:
    """
    Transcribes a voice file to text

    This will take an audio file and create and transcribe a text file from the audio source. The transcription
    will appear as a text response from the assistant.  It will be copied to the clipboard.
    """

    try:
        with open(choice, "rb") as audio_file:
            content = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text")
            logger.info("Speech to text content returned")
            return content
    except (FileNotFoundError, PermissionError, OSError) as e:
        content = handle_file_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content


def text_to_speech(client, model, voice, text, path) -> str:
    """
    Text to speech

    This will take text from a user prompt and create an audio file using a specified voice (TTS_VOICE).
    The new file will default to 'speech.mp3' and will be saved to the Desktop.
    """

    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text)
        file_name, _ = QFileDialog.getSaveFileName(
            None,
            "Save File",
            path,
            "MP3 Files (*.mp3)",)
        if file_name:
            response.stream_to_file(file_name)
            content = f"{file_name} succesfully created"
            logger.info("Text to speech content returned")
            return content
        else:
            content = "No file selected."
            logger.info("No file selected for saving.")
            return content

    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content
