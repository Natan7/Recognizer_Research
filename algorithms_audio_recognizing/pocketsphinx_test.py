### pip install pocketsphinx
import os
from pocketsphinx import AudioFile, get_model_path

#for phrase in AudioFile("../data/materias_coletadas/18-04-24-_gabriel_correa_ma-_barco_para_-_ra_fp.txt.wav"): print(phrase) # => "go forward ten meters"

model_path = get_model_path()

config = {
    'verbose': False,
    'audio_file': '../data/materias_coletadas/18-04-24-_gabriel_correa_ma-_barco_para_-_ra_fp.txt.wav',
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'model'),
    'lm': os.path.join(model_path, 'model.lm.bin'),
    'dict': os.path.join(model_path, 'model.dict')
}

audio = AudioFile(**config)
for phrase in audio:
    print(phrase)
