import logging
import openai
import base64
from PIL import Image
from io import BytesIO

from errors import (handle_openai_errors,
                    handle_file_errors,
                    handle_request_errors)

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


def generate_image(client, model, quality, text, size, path) -> str:
    """
    Image generator

    This will allow the user to input a prompt and openAI will create an image based on the 'text';  'model' is the image model that will be used (ie gpt-image-1); 'size' is the size of the image (ie 1024x1024);  quality comes from the reasoning/quality radio button, path is set in the config.ini file, number of images is set to 1.
    """

    try:
        result = client.images.generate(
            model=model,
            prompt=text,
            quality=quality,
            size=size,
            n=1,
        )
        
        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        image = Image.open(BytesIO(image_bytes))
        image.save(path, format="JPEG", quality=80, optimize=True)
        image.show()

        content = "Image generated successfully. Check the Desktop file 'image.jpg'."
        return content
    
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content


def describe_image(api_key, model, max_tokens, image_path, prompt) -> str:
    """The user can select an image and ask for a description"""

    import requests
    from requests.exceptions import HTTPError, Timeout, RequestException
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    except (OSError, FileNotFoundError, PermissionError) as e:
        content = handle_file_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content
    user_text = prompt
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": [{
            "type": "text",
            "text": user_text}, {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}}]}]}
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
    except (HTTPError, Timeout, RequestException, Exception) as e:
        content = handle_request_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content
    try:
        content = data["choices"][0]["message"]["content"]
        return content
    except ValueError:
        error = data["error"]["message"]
        logger.exception("This is an exception trace.", exc_info=True)
        return error
