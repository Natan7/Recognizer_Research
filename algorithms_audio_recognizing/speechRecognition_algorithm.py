import os
import time
import speech_recognition as sr
from output_recognizer import output

async def speechRecognition(wav_file, file_name, folder, is_record_time):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(wav_file)

    with audio as source:
        # Ajusta para o ruído de fundo se necessário
        recognizer.adjust_for_ambient_noise(source)
        audio_file = recognizer.record(source)
    
    start_time = time.time()  # Marca o início do tempo
    
    try:
        response = recognizer.recognize_google(audio_file, language="pt-BR")
    except sr.UnknownValueError:
        response = "Não consegui entender o áudio."
    except sr.RequestError as e:
        response = f"Erro ao se conectar ao serviço de reconhecimento: {e}"
    
    end_time = time.time()  # Marca o fim do tempo

    output(folder, file_name, response)
    
    if(is_record_time):
      execution_time = end_time - start_time # Calcula o tempo de execução
      output(f"{folder}time_", file_name, f"Tempo_de_execução: {execution_time} segundos")

    return response