import configparser

cfg = configparser.ConfigParser()
cfg.read("config.ini")

GPT3_MODEL = cfg["OPENAI"]["GPT3_MODEL"]
GPT4_MODEL = cfg["OPENAI"]["GPT4_MODEL"]
CODE_REVIEW_MODEL = cfg["OPENAI"]["GPT4_MODEL"]
FREQ_PENALTY = float(cfg["OPENAI"]["FREQ_PENALTY"])
CHAT_TEMP = float(cfg["OPENAI"]["CHAT_TEMP"])
TUTOR_TEMP = float(cfg["OPENAI"]["TUTOR_TEMP"])
IMG_MODEL = cfg["OPENAI"]["IMG_MODEL"]
QUALITY = cfg["OPENAI"]["QUALITY"]
VISION_MODEL = cfg["OPENAI"]["VISION_MODEL"]
WHISPER_MODEL = cfg["OPENAI"]["WHISPER_MODEL"]
TTS_MODEL = cfg["OPENAI"]["TTS_MODEL"]
TTS_VOICE = cfg["OPENAI"]["TTS_VOICE"]
MAX_TOKENS = float(cfg["OPENAI"]["MAX_TOKENS"])


def get_model_names(client, option) -> str:
    """List either the GPT models, or all models available through the API"""

    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    if option:
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
        "QUALITY:": QUALITY,
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
