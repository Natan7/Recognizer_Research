import os
import speech_recognition as sr
from pydub import AudioSegment
from output_recognizer import output

def speechRecognition(mp3_file, file_name, folder):
    ### Convert to .wav
    wav_file = os.path.splitext(os.path.basename(mp3_file))[0] + '.wav'
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export("../data/materias_coletadas/" + wav_file, format="wav")
    ###
    
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300;
    audio = sr.AudioFile('../data/materias_coletadas/'+ wav_file)

    with audio as source:
      audio_file = recognizer.record(source)
    
    response = recognizer.recognize_google(audio_file, language="pt-BR")
    output(folder, file_name, response)
    return response