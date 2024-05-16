import openai

from errors import handle_openai_errors


def chat(client, model, temperature, frequency_penalty, option, user_text, tutor_text="") -> str:
    """
    This is an openai chatbot.  

    The options are model (gpt-3.5, etc.);  temperature; freqency_penalty and option (1 for general chat and 0 for specific tutoring). All resonses will be displayed and copied to the clipboard.
    """

    try:
        if option == 1:
            initial_prompt = ("""You are a question answering expert. 
                              You have a wide range of
                              knowledge and are a world class expert in all things.  
                              When asked questions that require computations, take 
                              them one step at a time. If appropriate, give an example 
                              to help the user understand your answer.""")
        elif option == 0:
            initial_prompt = (f"""You are a world class expert in the field of 
                              {tutor_text}. You will answer the user's 
                              questions with enough detail that the user will be able 
                              to understand how you arrived at the answer.
                              Your answers can include examples if that will help 
                              the user better understand your answer.""")
        else:
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
