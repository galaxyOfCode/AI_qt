

def help_text():
    content = "AI Assistant Help\n\nButtons: Click the button that corresponds to the task you wish to perform. See below for info on each button. Press Enter after your selection has been made and the appropriate text boxes filed out.\n\nChat 3.5: General knowledge inquiry using the chatGPT 3.5 model (quicker than 4.0 below). Settings are for more creative responses than the Tutor choices below. Your question goes in the text box under 'You:'. Leave the 'Tutor:' box empty. The response will be shown in the 'Assistant:' box.\n\nChat 4.0:  Same as Chat 3.5 but uses the chatGPT 4.0 model (more accurate answers than 3.5).\n\nTutor 3.5: You will be able to specify what area of knowledge the response will be focused on.  This will use the 3.5 model but the settings will be for more precise responses (less creativity). Your question goes in the text box under “You:”. Enter your knowledge subject in the 'Tutor:' box. The response will be shown in the 'Assistant:' box.\n\nTutor 4.0: Same as Tutor 3.5 but uses the chatGPT 4.0 model (more accurate answers than 3.5).\n\nCode Review: Leave 'Tutor:' and 'You:' empty. You will be prompted for a code file to open.  A review of the code will be performed and displayed in 'Assistant:'. \n\nImage Gen: Enter a description of an image you would like to be created. A url will be returned in the 'Assistant:' box that you can copy into a web browser to view the image.\n\nVision: Leave all text boxes empty. You will be prompted for an image file (.png). An analysis of what the image contains will be returned in 'Assistant'.\n\nSpeech-to-Text: Leave all text boxes empty. You will be prompted for an audio file (.mp3). A transcript of the audio file will be returned in 'Assistant'. \n\nText-to-Speech: Enter text in the 'You:' box. An audio file will be returned in 'Assistant:' containing the text entered. \n\nList GPT: Returns current GPT models available through the openAI API. \n\nList All: Returns all models available though the openAI API. \n\nList Settings: Returns the current 'hard coded' settings used in this app."
    return content
