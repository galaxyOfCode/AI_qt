import subprocess


def get_model_names(client) -> str:
    """List either the GPT models, or all models available through the API"""

    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    header = "Current openAI Models:\n\n"
    model_ids.sort()
    content = ("\n".join(model_ids))
    return header + content


def get_settings(config) -> str:
    """ Print all hardcoded 'Magic Numbers' """

    settings = {
        "MODEL_LIST:": config.MODEL_LIST,
        "IMG_MODEL:": config.IMG_MODEL,
        "IMG_SIZE:": config.IMG_SIZE,
        "QUALITY:": config.QUALITY,
        "WHISPER_MODEL:": config.WHISPER_MODEL,
        "TTS_MODEL:": config.TTS_MODEL,
        "TTS_VOICE:": config.TTS_VOICE,
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
        content = (f"{package} updated to version {updated_version}")
    else:
        content = (
            f"\n{package} is already up to date: ({original_version})\n")
    return content


def check_package_version(package_name) -> str | None:
    """Returns the version number of a python package"""

    try:
        result = subprocess.check_output(
            ["pip", "show", package_name], stderr=subprocess.DEVNULL).decode("utf-8")
        for line in result.split('\n'):
            if line.startswith('Version:'):
                return line.split(': ')[1]
    except subprocess.CalledProcessError:
        return "error"
