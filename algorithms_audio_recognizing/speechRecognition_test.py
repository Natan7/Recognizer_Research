import speech_recognition as sr
from pydub import AudioSegment

### Convert to .wav
sound = AudioSegment.from_mp3("../Web_Scraping_EBC/materias_coletadas/19-04-24_-_gabriel_brum_-_passaportes_ra_ps.mp3")
sound.export("../Web_Scraping_EBC/materias_coletadas/19-04-24_-_gabriel_brum_-_passaportes_ra_ps.wav", format="wav")
###

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300;
audio = sr.AudioFile('../Web_Scraping_EBC/materias_coletadas/19-04-24_-_gabriel_brum_-_passaportes_ra_ps.wav')

with audio as source:
  audio_file = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio_file, language="pt-BR")
    print("Você disse: " + text)
except:
    print("erro ")