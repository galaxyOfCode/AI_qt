import subprocess


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


def get_settings(config) -> str:
    """ Print all hardcoded 'Magic Numbers' """

    settings = {
        "GPT3_MODEL:": config.GPT3_MODEL,
        "GPT4_MODEL:": config.GPT4_MODEL,
        "CODE_REVIEW_MODEL:": config.GPT4_MODEL,
        "IMG_MODEL:": config.IMG_MODEL,
        "QUALITY:": config.QUALITY,
        "VISION_MODEL:": config.VISION_MODEL,
        "WHISPER_MODEL:": config.WHISPER_MODEL,
        "TTS_MODEL:": config.TTS_MODEL,
        "TTS_VOICE:": config.TTS_VOICE,
        "TUTOR_TEMP:": config.TUTOR_TEMP,
        "CHAT_TEMP:": config.CHAT_TEMP,
        "FREQ_PENALTY:": config.FREQ_PENALTY,
        "MAX_TOKENS:": config.MAX_TOKENS}
    longest_key_length = max(len(key) for key in settings)
    content = "Current Settings:\n\n"
    for key, value in settings.items():
        buffer = " " * (longest_key_length - len(key))
        content += f"{key}{buffer}\t{value}\n"
    return content


def update() -> str:
    """Updates the 'openai' package"""

    package = "openai"
    original_version = check_package_version(package)
    subprocess.check_call(["pip", "install", "--upgrade",
                          "openai"], stdout=subprocess.DEVNULL)
    updated_version = check_package_version(package)
    if original_version == "error" or updated_version == "error":
        content = ("\nopenai package not found\n")
    if original_version != updated_version:
        content = (f"OpenAI updated to version {updated_version}")
    else:
        content = (f"\nOpenAI is already up to date ({original_version})\n")
    return content


def check_package_version(package_name):
    """Returns the version number of a python package"""

    try:
        result = subprocess.check_output(
            ["pip", "show", package_name], stderr=subprocess.DEVNULL).decode("utf-8")
        for line in result.split('\n'):
            if line.startswith('Version:'):
                return line.split(': ')[1]
    except subprocess.CalledProcessError:
        return "error"
