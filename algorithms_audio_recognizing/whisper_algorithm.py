import time
import whisper as wp
from output_recognizer import output

async def whisper(mp3_file, file_name, folder):
    speech_model = wp.load_model("small")

    start_time = time.time() # Marca o início do tempo

    try:
        # Transcreve o áudio
        response = speech_model.transcribe(mp3_file)
        transcribed_text = response["text"]  # Acessa o texto transcrito
    except Exception as e:
        transcribed_text = f"Erro na transcrição: {e}"

    end_time = time.time() # Marca o fim do tempo

    execution_time = end_time - start_time # Calcula o tempo de execução
    output(f"{folder}time_", file_name, f"Tempo_de_execução: {execution_time} segundos")
    output(folder, file_name, transcribed_text)
  
    return transcribed_text