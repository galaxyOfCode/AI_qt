import openai

from errors import handle_openai_errors


def chat(client, model, temperature, frequency_penalty, user_text) -> str:
    """
    This is an openai chatbot.  

    The options are model (gpt-3.5, etc.);  temperature and freqency_penalty. All responses will be displayed and copied to the clipboard.
    """

    try:
        initial_prompt = ("""The user is a Computer Science university student. He prefers to code in Python and also does website development that includes php. He only uses a Mac computer, so he doesn't need any instructions related to 'Windows PCs.'  He uses VS Code as his primary IDE. He learns best with explanations followed by an example.""")

        messages = [{"role": "system", "content": initial_prompt}]
        messages.append({"role": "user", "content": user_text})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            frequency_penalty=frequency_penalty)

        content = response.choices[0].message.content
        return content
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        return content
