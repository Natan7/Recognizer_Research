import os
import re
import asyncio
from pydub import AudioSegment
from file_lister import mp3_files
from output_recognizer import output
from whisper_algorithm import whisper
from speechRecognition_algorithm import speechRecognition
from assemblyai_algorithm import assemblyai
import Levenshtein

#
# Cortar o arquivo MP3 em segmentos de n segundos
#
async def cut_mp3_by_time(input_file, file_name, output_directory, seconds, on_star):
    # Carrega o arquivo MP3 usando pydub
    audio = AudioSegment.from_mp3(input_file)
    
    # n segundos em milissegundos
    segment_duration = seconds * 1000
    
    # Cria o diretório de saída se não existir
    os.makedirs(output_directory, exist_ok=True)
    
    if(on_star):
        start_time = 0
        end_time = segment_duration
        segment = audio[start_time:end_time]

        # Nome do arquivo de saída baseado no nome original
        output_file = os.path.join(output_directory, f"{file_name}.mp3")
    else:
        audio_duration = len(audio)

        start_time = audio_duration - segment_duration
        end_time = audio_duration
        segment = audio[start_time:end_time]

        # Nome do arquivo de saída baseado no nome original
        output_file = os.path.join(output_directory, f"{file_name}_last_{seconds}_seconds.mp3")

    # Exporta os n segundos como um arquivo MP3
    segment.export(output_file, format="mp3")

#
# Coletar texto de uma arquivo .txt
#
async def get_text_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        phrase = file.read().strip()
    return phrase

#
# Remove palavras duplicadas de um conjunto
#
async def remove_duplicates_from_set(input_set):
    unique_list = list(input_set)
    unique_set = set(unique_list)
    return unique_set

#
# Retorna a quantidade de palavras em comum de um conjunto (frase)
#
async def count_common_words(set1, set2):
    set1_lower = {word.lower() for word in set1}
    set2_lower = {word.lower() for word in set2}
    
    common_words = set1_lower.intersection(set2_lower)
    return len(common_words)

#
# Retorna as 3 ultimas palavras de uma frase
#
async def get_last_three_words(phrase):
    words = phrase.split()
    
    if len(words) < 3:
        return "Phrase does not contain enough words."
    
    last_words = words[-3:]    
    return ' '.join(last_words)

#
# Encontrar frase no texto completo e retorna o grau de similaridade da frase parágrafo da frase e texto sem o parágrafo
#
async def find_by_word(all_text, phrase):
    best_match_position = -1
    max_match_count = -1
    phrase_found = ""
    truncated_text = ""

    # Dividir o texto em frases
    text_phrases = all_text.split('.')
    words = phrase.split()

    # Iterar sobre cada frase no texto
    for idx, phrase in enumerate(text_phrases):
        unique_set = await remove_duplicates_from_set(phrase.split())
        match_count = await count_common_words(unique_set, words)
        if(max_match_count<match_count & match_count>3):
            max_match_count = match_count
            best_match_position = idx
            phrase_found = phrase.strip()

    for idx, phrase in enumerate(text_phrases):
        if(idx<best_match_position):
            truncated_text += phrase + "."

    return max_match_count, phrase_found, truncated_text

#
# Retorna a posição exata no texto de um conjunto de palavras
#
async def find_position_of_consecutive_words(phrase, target_words):
    words = re.split(r'[,\s]+', phrase.lower())
    min_distance = 1000
    index = -1

    # Checa se o conjunto de palavras é maior que 3
    if len(target_words) != 3:
        raise ValueError("The target words list must contain exactly three words.")
    
    for i in range(len(words) - 2):
        if (words[i:i+3] == target_words):
            return i + 3
        elif(Levenshtein.distance(words[i:i+3], target_words)<=min_distance):
            min_distance = Levenshtein.distance(words[i:i+3], target_words)
            index = i + 3
    
    return index

#
# Realiza conversão audios em .mp3 para .wav
#
async def convert_to_wav(mp3_file, folder):
    wav_file = os.path.splitext(os.path.basename(mp3_file))[0] + '.wav'
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(f"{folder}/{wav_file}", format="wav")

#
# Realiza o truncamento das matérias dos audios e textos
#
async def truncate_news(file_txt_name, mp3_file, path_truncated_mp3):
    await cut_mp3_by_time(mp3_file, os.path.splitext(os.path.basename(mp3_file))[0], "../data/step3_truncated_news/", 30, True)
    await convert_to_wav(path_truncated_mp3, "../data/step3_truncated_news/")

    await cut_mp3_by_time(path_truncated_mp3, os.path.splitext(os.path.basename(mp3_file))[0], "../data/step2_last_words_news/", 5, False)
    path_last_words_mp3 = "../data/step2_last_words_news/" + os.path.splitext(os.path.basename(mp3_file))[0] + "_last_5_seconds.mp3"
    await convert_to_wav(path_last_words_mp3, "../data/step2_last_words_news/")
    
    path_last_words_mp3 = "../data/step2_last_words_news/" + os.path.splitext(os.path.basename(mp3_file))[0] + "_last_5_seconds.wav"
    await speechRecognition(path_last_words_mp3, file_txt_name, '../data/step2_last_words_news/', False)

    phrase_file = '../data/step2_last_words_news/' + file_txt_name
    original_text_file = '../data/step1_news_colected/' + file_txt_name
    last_phrase = await get_text_file(phrase_file)
    all_text = await get_text_file(original_text_file)
    last_three_words = await get_last_three_words(last_phrase)

    max_match_count, phrase_found, truncated_text = await find_by_word(all_text, last_phrase)
    if(max_match_count>0):
        index_last_word = await find_position_of_consecutive_words(phrase_found, last_three_words.split())
        if(index_last_word>0):
            words = phrase_found.split()
            last_phrase = words[:index_last_word]
            text_final = truncated_text + ' ' + ' '.join(last_phrase)
            output( '../data/step3_truncated_news/', file_txt_name, text_final)

####################################################################
############################### Main ###############################
####################################################################
async def main():
    path_files = "../data/step1_news_colected"
    list_mp3_file = mp3_files(path_files)
    
    for mp3_file in list_mp3_file:
        file_txt_name = os.path.splitext(os.path.basename(mp3_file))[0] + '.txt'
        path_truncated_mp3 = "../data/step3_truncated_news/" + os.path.splitext(os.path.basename(mp3_file))[0] + ".mp3"
        await truncate_news(file_txt_name, mp3_file, path_truncated_mp3)
    
    path_truncated_files = "../data/step3_truncated_news"
    list_mp3_file = mp3_files(path_truncated_files)
    for mp3_file in list_mp3_file:
        file_txt_name = os.path.splitext(os.path.basename(mp3_file))[0] + '.txt'
        path_truncated_mp3 = "../data/step3_truncated_news/" + os.path.splitext(os.path.basename(mp3_file))[0] + ".mp3"
        path_truncated_wav = "../data/step3_truncated_news/" + os.path.splitext(os.path.basename(mp3_file))[0] + ".wav"
        await whisper(path_truncated_mp3, file_txt_name, '../data/result_whisper/')
        await assemblyai(path_truncated_mp3, file_txt_name, '../data/result_assemblyai/')
        await speechRecognition(path_truncated_wav, file_txt_name, '../data/result_speechRecognition/', True)
    
asyncio.run(main())
####################################################################
####################################################################
####################################################################