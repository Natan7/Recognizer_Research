### pip install pocketsphinx
#from pocketsphinx import AudioFile

##for phrase in AudioFile("../Web_Scraping_EBC/materias_coletadas/19-04-24_-_gabriel_brum_-_passaportes_ra_ps.wav"): print(phrase) # => "go forward ten meters"


import os
from pocketsphinx import AudioFile, get_model_path

model_path = get_model_path()

config = {
    'verbose': False,
    'audio_file': '../Web_Scraping_EBC/materias_coletadas/19-04-24_-_gabriel_brum_-_passaportes_ra_ps.wav',
    'hmm': get_model_path('en-us'),
    'lm': get_model_path('en-us.lm.bin'),
    'dict': get_model_path('cmudict-en-us.dict')
    #'hmm': get_model_path('pt-br'),
    #'lm': get_model_path('pt-br.lm.bin'),
    #'dict': get_model_path('cmudict-pt-br.dict')
}

audio = AudioFile(**config)
for phrase in audio:
    print(phrase)