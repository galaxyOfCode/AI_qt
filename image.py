import openai
import pyperclip
import errors


def image(client, model, quality, text) -> str:
    '''
    Image generator

    This will allow the user to input a prompt and openAI will create an image based on the 'text''.  'model' is the image model that will be used (ie Dall-e-3). 'size' is the size of the image (ie 1024x1024).  Number of images is set to 1.
    '''
    try:
        res = client.images.generate(
            model=model,
            prompt=text,
            quality=quality,
        )
        image_url = res.data[0].url
        pyperclip.copy(image_url)
        return image_url
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = errors.handle_openai_errors(e)
        return content


def vision(api_key, model, max_tokens, image_path) -> str:
    '''
    The user can select an image and ask for a description
    '''
    import requests
    import base64
    from requests.exceptions import HTTPError, Timeout, RequestException
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    except (OSError, FileNotFoundError, PermissionError) as e:
        content = errors.handle_file_errors(e)
        return content
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
    except (HTTPError, Timeout, RequestException, Exception) as e:
        content = errors.handle_request_errors(e)
        return content
    try:
        content = data["choices"][0]["message"]["content"]
        pyperclip.copy(content)
        return content
    except:
        error = data["error"]["message"]
        return error
