import os
import time
from dotenv import load_dotenv
import assemblyai as aai
from output_recognizer import output

# Chave de acesso gratuita
load_dotenv()
aai.settings.api_key = os.getenv("AI_KEY")

TRANSCRIBER = aai.Transcriber(config=aai.TranscriptionConfig(language_code='pt'))

async def assemblyai(mp3_file, file_name, folder):
    start_time = time.time() # Marca o início do tempo

    try:
        response = await TRANSCRIBER.transcribe(mp3_file)  # Use await se for uma operação assíncrona
        transcribed_text = response.text
    except Exception as e:
        transcribed_text = f"Erro na transcrição: {e}"
    
    end_time = time.time() # Marca o fim do tempo

    execution_time = end_time - start_time # Calcula o tempo de execução
    output(f"{folder}time_", file_name, f"Tempo_de_execução: {execution_time} segundos")
    output(folder, file_name, transcribed_text)

    return transcribed_text