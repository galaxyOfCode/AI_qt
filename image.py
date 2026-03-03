import base64
from io import BytesIO
import logging
import openai
from PIL import Image
from requests.exceptions import HTTPError, Timeout, RequestException

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


def generate_image(client: openai.OpenAI, model: str, quality: str, text: str, size: str, path) -> str:
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
        logger.info("Image generated successfully.")
        return content
    
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content


def describe_image(client: openai.OpenAI, model: str, image_path: str, prompt: str) -> str:
    """Uses OpenAI SDK to describe a local image via base64 encoding."""
    
    try:
        with open(image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode("utf-8")
    except (OSError, FileNotFoundError, PermissionError) as e:
        logger.exception("File access error.")
        return f"File error: {str(e)}"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        logger.exception("OpenAI API error.")
        return f"API error: {str(e)}"
    except Exception as e:
        logger.exception("Unexpected error.")
        return f"Unexpected error: {str(e)}"