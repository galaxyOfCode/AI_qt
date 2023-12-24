def help_text():
    ''' Contents of the help file '''

    content = ("AI Assistant Help\n\n"

               "Buttons: Click the button that corresponds to the task you wish to perform. See below for info on each button. Press Enter after your selection has been made and the appropriate text boxes filed out.\n\n"

               "Chat 3.5: General knowledge inquiry using the chatGPT 3.5 model (quicker than 4.0 below). Settings are for more creative responses than the Tutor choices below. Your question goes in the text box under 'User:'. Leave the 'Tutor:' box empty. The response will be shown in the 'Assistant:' box.\n\n"

               "Chat 4.0:  Same as Chat 3.5 but uses the chatGPT 4.0 model (more accurate answers than 3.5).\n\n"

               "Tutor 3.5: You will be able to specify what area of knowledge the response will be focused on.  This will use the 3.5 model but the settings will be for more precise responses (less creativity). Your question goes in the text box under 'User:'. Enter your subject area (ie Physics) in the 'Tutor:' box. The response will be shown in the 'Assistant:' box.\n\n"

               "Tutor 4.0: Same as Tutor 3.5 but uses the chatGPT 4.0 model (more accurate answers than 3.5).\n\n"

               "Code Review: Leave 'Tutor:' and 'User:' empty. You will be prompted for a code file to open.  A review of the code will be performed and displayed in 'Assistant:'.\n\n"

               "Image Gen: Enter a description of an image you would like to be created. A url will be returned in the 'Assistant:' box that you can copy into a web browser to view the image.\n\n"

               "Vision: Leave all text boxes empty. You will be prompted for an image file (.jpg or .png). An analysis of what the image contains will be returned in 'Assistant'.\n\n"
               
               "Speech-to-Text: Leave all text boxes empty. You will be prompted for an audio file (.mp3). A transcript of the audio file will be returned in 'Assistant'.\n\n"

               "Text-to-Speech: Enter some text in the 'User:' box. You will be asked to save a file that will contain an audio recording of the text entered (using the voice stated in the TTS_VOICE setting.\n\n"

               "List GPT: Returns current GPT models available through the openAI API. \n\n"

               "List All: Returns all models available though the openAI API.\n\n"

               "List Settings: Returns the current 'hard coded' settings used in this app.")
    return content
