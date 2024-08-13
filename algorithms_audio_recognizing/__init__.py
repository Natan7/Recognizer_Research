import os
from pydub import AudioSegment
from file_lister import mp3_files
from output_recognizer import output
from whisper_algorithm import whisper
from speechRecognition_algorithm import speechRecognition
from assemblyai_algorithm import assemblyai
from thefuzz import fuzz
import re

path_files = "../data/step1_materias_coletadas"
list_mp3_file = mp3_files(path_files)
##print(list_mp3_file)

# Função para cortar o arquivo MP3 em segmentos de 30 segundos
def cut_mp3(input_file, file_name, output_directory):
    # Carrega o arquivo MP3 usando pydub
    audio = AudioSegment.from_mp3(input_file)
    
    # Duração desejada de cada segmento em milissegundos
    segment_duration = 30 * 1000  # 30 segundos em milissegundos   
    
    # Cria o diretório de saída se não existir
    os.makedirs(output_directory, exist_ok=True)
    
    # Corta o arquivo em segmentos de 30 segundos
    start_time = 0
    end_time = segment_duration
    segment = audio[start_time:end_time]
    segment.export(os.path.join(output_directory, f"{file_name}.mp3"), format="mp3")
    #print(f"Segmento {file_name} cortado com sucesso.")

# Função para cortar os últimos 5 segundos do arquivo MP3
def cut_last_5_seconds(input_file, file_name, output_directory):
    # Carrega o arquivo MP3 usando pydub
    audio = AudioSegment.from_mp3(input_file)
    
    # Duração dos últimos 5 segundos em milissegundos
    last_5_seconds_duration = 5 * 1000  # 5 segundos em milissegundos
    
    # Obtém a duração total do áudio em milissegundos
    audio_duration = len(audio)
    
    # Corta os últimos 5 segundos do áudio
    start_time = audio_duration - last_5_seconds_duration
    end_time = audio_duration
    last_5_seconds = audio[start_time:end_time]
    
    # Nome do arquivo de saída baseado no nome original
    output_file = os.path.join(output_directory, f"{file_name}_last_5_seconds.mp3")
    
    # Exporta os últimos 5 segundos como um arquivo MP3
    last_5_seconds.export(output_file, format="mp3")
    print(f"Últimos 5 segundos do áudio cortados com sucesso.")


########################## Levenshtein ###########################
##################################################################

import Levenshtein

def match_palavras(conjunto, palavra_consulta, limite):
    matches = []
    for palavra in conjunto:
        distancia = Levenshtein.distance(palavra, palavra_consulta)
        if distancia <= limite:
            matches.append((palavra, distancia))
    return matches

def ler_frase_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        frase = arquivo.read().strip()
    return frase

def encontrar_frase_com_distancia_menor(texto, frase, limite):
    menor_distancia = float('inf')
    posicao_menor_distancia = -1
    frase_encontrada = ""

    # Dividir o texto em frases
    frases_no_texto = texto.split('.')

    # Iterar sobre cada frase no texto
    for idx, frase_no_texto in enumerate(frases_no_texto):
        # Calcular a distância de Levenshtein entre a frase no texto e a frase de consulta
        distancia = Levenshtein.distance(frase_no_texto.strip(), frase.strip())
        
        # Verificar se a distância é menor que o limite e se é a menor encontrada até agora
        if distancia <= limite and distancia < menor_distancia:
            menor_distancia = distancia
            posicao_menor_distancia = idx
            frase_encontrada = frase_no_texto.strip()

    return posicao_menor_distancia, menor_distancia, frase_encontrada


def remove_duplicates_from_set(input_set):
    # Convert set to list (to remove duplicates)
    unique_list = list(input_set)
    
    # Optionally convert back to set if you need a set without duplicates
    unique_set = set(unique_list)
    
    return unique_set


def count_matching_words(set1, set2):
    # Convert sets to lowercase if case sensitivity is not required
    set1_lower = {word.lower() for word in set1}
    set2_lower = {word.lower() for word in set2}
    
    # Find intersection of the two sets
    common_words = set1_lower.intersection(set2_lower)
    
    # Return the count of common words
    return len(common_words)

def find_position_of_consecutive_words(phrase, target_words):
    # Split the phrase into a list of words
    words = re.split(r'[,\s]+', phrase.lower())
    min_distance = 1000
    index = -1

    # Ensure the target words list contains exactly three words
    if len(target_words) != 3:
        raise ValueError("The target words list must contain exactly three words.")
    
    # Find the index of the first of the target words in the list
    for i in range(len(words) - 2):  # We go up to len(words) - 2 to avoid out of range errors
        if (words[i:i+3] == target_words):
            return i + 3 # Return the starting index of the sequence
        elif(Levenshtein.distance(words[i:i+3], target_words)<min_distance):
            min_distance = Levenshtein.distance(words[i:i+3], target_words)
            index = i + 3
    
    return index  # Return the starting index of the sequence or -1 if the sequence is not found


def get_last_three_words(phrase):
    # Split the phrase into a list of words
    words = phrase.split()
    
    # Check if there are at least two words
    if len(words) < 3:
        return "Phrase does not contain enough words."
    
    # Get the last two words
    last_two_words = words[-3:]
    
    # Join them back into a single string
    return ' '.join(last_two_words)

#################################
#### Encontrar frase no texto ###
def find_by_word(texto, frase):
    menor_distancia = float('inf')
    posicao_menor_distancia = -1
    frase_encontrada = ""

    # Dividir o texto em frases
    frases_no_texto = texto.split('.')

    palavras_frase = frase.split()
    max_matching_count = -1
    texto_truncado = ""
    # Iterar sobre cada frase no texto
    for idx, frase_no_texto in enumerate(frases_no_texto):
        unique_set = remove_duplicates_from_set(frase_no_texto.split())
        matching_count = count_matching_words(unique_set, palavras_frase)
        if(max_matching_count<matching_count & matching_count>3):
            max_matching_count = matching_count
            posicao_menor_distancia = idx
            frase_encontrada = frase_no_texto.strip()

    for idx, frase_no_texto in enumerate(frases_no_texto):
        if(idx<posicao_menor_distancia):
            texto_truncado += frase_no_texto + "."

    return max_matching_count, frase_encontrada, texto_truncado
    
for mp3_file in list_mp3_file:
    file_name = os.path.splitext(os.path.basename(mp3_file))[0] + '.txt'
    
    #cut_mp3(mp3_file, os.path.splitext(os.path.basename(mp3_file))[0], "../data/step2_materias_truncadas/")
    #path_mp3 = "../data/step2_materias_truncadas/" + os.path.splitext(os.path.basename(mp3_file))[0] + ".mp3"
    #cut_last_5_seconds(path_mp3, os.path.splitext(os.path.basename(mp3_file))[0], "../data/step3_materias_ultimas_palavras/")

    #path2_mp3 = "../data/step3_materias_ultimas_palavras/" + os.path.splitext(os.path.basename(mp3_file))[0] + "_last_5_seconds.mp3"
    #speechRecognition(path2_mp3, file_name, '../data/step4_ultimas_palavras/')

    # Levenshtein:
    arquivo_frase = '../data/step4_ultimas_palavras/' + file_name
    arquivo_completo = '../data/step1_materias_coletadas/' + file_name
    ##conjunto_palavras = {"aconteceu enquanto a escritora caminhava próximo"}

    frase_consulta = ler_frase_de_arquivo(arquivo_frase)
    texto_completo_consulta = ler_frase_de_arquivo(arquivo_completo)
    
    # Dividir o texto em palavras
    palavras = texto_completo_consulta.split()

    # Converter a lista de palavras em um conjunto (set) para obter palavras únicas
    conjunto_palavras = set(palavras)
    
   # Example usage
    last_three_words = get_last_three_words(frase_consulta)
    print(last_three_words.split())  # Output: "example phrase"

    distancia, frase_encontrada, texto_truncado = find_by_word(texto_completo_consulta, frase_consulta)
    if(distancia>0):
        print(f"Frase consulta: {frase_consulta}")
        print(f"Distancia match: {distancia}")
        print(f"Frase encontrada: {frase_encontrada}")
        print("==========TEXTO TRUNCADO===========")
        print(texto_truncado)
        print()
        position = find_position_of_consecutive_words(frase_encontrada, last_three_words.split())
        print(position)
        if(position>0):
            words = frase_encontrada.split()
            words_until_including = words[:position]
            text_final = texto_truncado + ' ' + ' '.join(words_until_including)
            print(text_final)
            ##output( '../data/step5_texto_final/', file_name, text_final)
        print()
        
    #whisper(mp3_file, file_name, '../data/textos_whisper/')
    #speechRecognition(mp3_file, file_name, '../data/textos_speechRecognition/')
    #assemblyai(mp3_file, file_name, '../data/textos_assemblyai/')