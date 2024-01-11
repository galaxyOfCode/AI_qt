import openai
import pyperclip
from errors import handle_openai_errors


def chat(client, model, temperature, frequency_penalty, option, text, tutor="") -> str:
    """
    This is an openai chatbot.  

    The options are model (gpt-3.5-turbo-1106, etc);  temperature; freqency_penalty
    and option (1 for general chat and 0 for specific tutoring). All resonses will be displayed and copied to the clipboard.
    """
    
    try:
        if option:
            initial_prompt = "You are a question answering expert. You have a wide range of knowledge and are a world class expert in all things.  When asked questions that require computations, take them one step at a time. If appropriate, give an example to help the user understand your answer."
            messages = [{"role": "system", "content": initial_prompt}]
        else:
            initial_prompt = f"You are a world class expert in the field of {tutor}. You will answer the users questions with enough detail that the user will be able to understand how you arrived at the answer.  Your answers can include examples if that will help the user better understand your answer."
            messages = [{"role": "system", "content": initial_prompt}]
        messages.append({"role": "user", "content": text})

        res = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            frequency_penalty=frequency_penalty
        )
        content = res.choices[0].message.content
        pyperclip.copy(content)
        return content
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        return content
