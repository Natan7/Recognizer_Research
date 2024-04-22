import os
from file_lister import mp3_files
from whisper_algorithm import whisper
from speechRecognition_algorithm import speechRecognition
from assemblyai_algorithm import assemblyai

path_files = "../data/materias_coletadas"
list_mp3_file = mp3_files(path_files)
print(list_mp3_file)

for mp3_file in list_mp3_file:
    file_name = os.path.splitext(os.path.basename(mp3_file))[0] + '.txt'
    #whisper(mp3_file, file_name, '../data/textos_whisper/')
    #speechRecognition(mp3_file, file_name, '../data/textos_speechRecognition/')
    #assemblyai(mp3_file, file_name, '../data/textos_assemblyai/')