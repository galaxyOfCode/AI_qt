import logging
import openai

from errors import handle_openai_errors

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

def chat(client, model, reasoning, user_text, r_flag) -> str:
    """
    This is an openai chatbot.  

    The options are model (gpt-3.5, etc.). All responses will be displayed and copied to the clipboard. r_flag is a flag that will be set to 1 if the user is using a model that requires a lot of reasoning and critical thinking.
    """
    
    try:
        initial_prompt = ("""The user is a Computer Science university student named Jeff. He prefers to code in Python and also does website development that includes php. He only uses a Mac computer, so he doesn't need any instructions related to 'Windows PCs.'  He uses VS Code as his primary IDE. He learns best with explanations followed by an example.""")
    
        if r_flag == 0:
            messages = [{"role": "system", "content": initial_prompt}]
            messages.append({"role": "user", "content": user_text})

            response = client.responses.create(
                model=model,
                input=messages)
        else:
            messages = [{"role": "user", "content": user_text}]

            response = client.responses.create(
                model=model,
                reasoning={"effort": reasoning},
                input=messages)
            
        content = response.output_text
        logger.info("Chat content returned")
        return content
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        logger.exception("This is an exception trace.", exc_info=True)
        return content
