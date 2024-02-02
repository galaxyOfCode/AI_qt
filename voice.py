import openai
from PyQt6.QtWidgets import QFileDialog
from errors import handle_file_errors, handle_openai_errors


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
                response_format="text"
            )
            return content
    except (FileNotFoundError, PermissionError, OSError) as e:
        content = handle_file_errors(e)
        return content
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
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
            input=text
        )
        file_name, _ = QFileDialog.getSaveFileName(
            None,
            "Save File",
            path,
            "MP3 Files (*.mp3)",
        )
        if file_name:
            response.stream_to_file(file_name)
            content = f"{file_name} succesfully created"
            return content
        else:
            content = "No file selected."
            return content

    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        return content
