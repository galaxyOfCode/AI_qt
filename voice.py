import openai
from PyQt6.QtWidgets import QFileDialog
import pyperclip


def whisper(client, model, choice):
    '''
    Transcribes a voice file to text

    This will take an audio file and create and transcribe a text file from the audio source. The transcription will appear as a text response from the assistant.  It will be copied to the clipboard.
    '''
    try:
        with open(choice, "rb") as audio_file:
            content = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text"
            )
            pyperclip.copy(content)
            return content
    except FileNotFoundError:
        content = (f"Error: The file {choice} was not found.")
        return content
    except PermissionError:
        content = (f"Error: Permission denied when trying to read {choice}.")
        return content
    except OSError:
        content = (
            f"Error: An error occurred while reading from the file {choice}.")
        return content


def tts(client, model, voice, text):
    '''
    Text to speech

    This will take text from a user prompt and create an audio file using a specified voice (TTS_VOICE). The new file will default to 'speech.mp3' and will be saved to the Desktop.
    '''
    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        file_name, _ = QFileDialog.getSaveFileName(
            None, 
            "Save File", 
            "/Users/jeffmacair/Desktop/speech.mp3", 
            "MP3 Files (*.mp3)", 
        )
        if file_name:
            response.stream_to_file(file_name)
            content = f"{file_name} succesfully created"
            return content
        else:
            content = "No file selected."
            return content
        
    except openai.APIConnectionError as e:
        content = "The server could not be reached\n" + e.__cause__
        return content
    except openai.RateLimitError as e:
        content = "A 429 status code was received; we should back off a bit."
        return content
    except openai.APIStatusError as e:
        content = "Another non-200-range status code was received" + \
            e.status_code + "\n" + e.response
        return content
