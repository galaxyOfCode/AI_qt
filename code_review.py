import openai
import pyperclip


def code_reviewer(client, model, file_path):
    '''
    Reviews a code file.
    
    Allows the user to select a file for openAI to review the code for
    style, performance, readability, and maintainability.  
    '''
    with open(file_path, "r") as file:
        content = file.read()
        initial_prompt = "You will receive a file's contents as text. Generate a code review for the file.  Indicate what changes should be made to improve its style, performance, readability, and maintainability.  If there are any reputable libraries that could be introduced to improve the code, suggest them.  Be kind and constructive.  For each suggested change, include line numbers to which you are referring."
        messages = [
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": f"Code review the following file: {content}"}
        ]
        try:
            res = client.chat.completions.create(
                model=model,
                messages=messages
            )
        except openai.APIConnectionError as e:
            content = "The server could not be reached" + e.__cause__
            return content
        except openai.RateLimitError as e:
            content = "A 429 status code was received; we should back off a bit."
            return content
        except openai.APIStatusError as e:
            content = "Another non-200-range status code was received" + e.status_code + e.response
            return content
        content = res.choices[0].message.content
        pyperclip.copy(content)
        return content
