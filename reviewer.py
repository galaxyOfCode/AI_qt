import logging
import openai

from errors import handle_openai_errors, handle_file_errors


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


def code_review(client, model, file_path) -> str:
    """
    Reviews a code file.

    Allows the user to select a file for openAI to review the code for
    style, performance, readability, and maintainability.  
    """

    try:
        with open(file_path, "r") as file:
            content = file.read()
            initial_prompt = ("""You will receive a file's contents as text. 
                              Generate a code review for the file.  
                              Indicate what changes should be made to improve its style, performance, readability, and maintainability.
                              If there are any reputable libraries that could be introduced to improve the code, suggest them.  Be kind and constructive.  For each suggested change, include line numbers to which you are referring.""")
            messages = [
                {"role": "system", "content": initial_prompt},
                {"role": "user", "content": f"Code review the following file: {content}"}]
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages)
            except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
                content = handle_openai_errors(e)
                logger.exception("This is an exception trace.", exc_info=True)
                return content
            content = response.choices[0].message.content
            logger.info("Code review content returned")
            return content
    except (FileNotFoundError, PermissionError, OSError) as e:
        content = handle_file_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content
