
def get_model_names(client, option) -> str:
    """List either the GPT models, or all models available through the API"""

    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    if option:
        model_ids = [
            model_id for model_id in model_ids if model_id.startswith("gpt")
        ]
        header = "Current openAI GPT Models:\n\n"
    else:
        header = "Current openAI Models:\n\n"
    model_ids.sort()
    content = ("\n".join(model_ids))
    return header + content


def get_settings(config) -> str:
    """ Print all hardcoded 'Magic Numbers' """

    settings = {
        "GPT3_MODEL:": config.GPT3_MODEL,
        "GPT4_MODEL:": config.GPT4_MODEL,
        "CODE_REVIEW_MODEL:": config.CODE_REVIEW_MODEL,
        "IMG_MODEL:": config.IMG_MODEL,
        "QUALITY:": config.QUALITY,
        "VISION_MODEL:": config.VISION_MODEL,
        "WHISPER_MODEL:": config.WHISPER_MODEL,
        "TTS_MODEL:": config.TTS_MODEL,
        "TTS_VOICE:": config.TTS_VOICE,
        "TUTOR_TEMP:": config.TUTOR_TEMP,
        "CHAT_TEMP:": config.CHAT_TEMP,
        "FREQ_PENALTY:": config.FREQ_PENALTY,
        "MAX_TOKENS:": config.MAX_TOKENS
    }
    longest_key_length = max(len(key) for key in settings)
    content = "Current Settings:\n\n"
    for key, value in settings.items():
        buffer = " " * (longest_key_length - len(key))
        content += f"{key}{buffer}\t{value}\n"
    return content
