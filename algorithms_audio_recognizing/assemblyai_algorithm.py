import os
from dotenv import load_dotenv
import assemblyai as aai
from output_recognizer import output

# Chave de acesso gratuita
load_dotenv()
aai.settings.api_key = os.getenv("AI_KEY")

TRANSCRIBER = aai.Transcriber(config=aai.TranscriptionConfig(language_code='pt'))

def assemblyai(mp3_file, file_name, folder):
    response = TRANSCRIBER.transcribe(mp3_file)
    output(folder, file_name, response.text)
    return response.text