import openai
import pyperclip


def image(client, model, size, style, text):
    '''
    Image generator

    This will allow the user to input a prompt and openAI will create an image based on the 'text''.  'model' is the image model that will be used (ie Dall-e-3). 'size' is the size of the image (ie 1024x1024).  Number of images is set to 1.
    '''
    try:
        res = client.images.generate(
            model=model,
            prompt=text,
            size=size,
            style=style,
            n=1
        )
        image_url = res.data[0].url
        pyperclip.copy(image_url)
        return image_url
    except openai.APIConnectionError as e:
        content = "The server could not be reached" + e.__cause__
        return content
    except openai.RateLimitError as e:
        content = "A 429 status code was received; we should back off a bit."
        return content
    except openai.APIStatusError as e:
        content = "Another non-200-range status code was received" + e.status_code + e.response
        return content


def encode_image(image_path):
    '''
    Helper function for vision()
    '''
    import base64
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except OSError as e:
        print(e)
        return ""


def vision(api_key, model, max_tokens, image_path):
    '''
    The user can select an image and ask for a description
    '''
    import requests
    from requests.exceptions import HTTPError, Timeout, RequestException
    base64_image = encode_image(image_path)
    if (base64_image == ""):
        return
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
    except HTTPError as http_err:
        content = (f"HTTP error occurred: {http_err}")
        return content
    except Timeout as timeout_err:
        content = (f"Request timed out: {timeout_err}")
        return content
    except RequestException as req_err:
        content = (f"Error during request: {req_err}")
        return content
    except Exception as e:
        content = (f"An unexpected error occurred: {e}")
        return content
    try:
        content = data["choices"][0]["message"]["content"]
        pyperclip.copy(content)
        return content
    except:
        error = data["error"]["message"]
        return error
