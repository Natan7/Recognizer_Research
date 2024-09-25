import os
import asyncio
from output_recognizer import output_append

#
# Coletar uma lista de textos .txt
#
def get_text_files(path_file):
    files = []
    for file_name in os.listdir(path_file):
        path = os.path.join(path_file, file_name)
        if os.path.isfile(path):
            if path.lower().endswith('.txt'):
                files.append(path)
    return files

#
# Coletar texto de uma arquivo .txt
#
def get_text_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        phrase = file.read().strip()
    return phrase


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#
# Verifica a simililaridade entre dois textos utilizando cosseno
#
def compute_cosine_similarity(text1, text2):
    # Create TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the texts
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    
    # Compute cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return similarity[0][0]

#
# Verifica a simililaridade entre dois textos utilizando Jaccard
#
def jaccard_similarity(text1, text2):
    # Tokenizando e criando conjuntos de palavras
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    
    # Calculando a Similaridade Jaccard
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union

from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn.functional as F

# Função para calcular a similaridade entre dois textos usando BERT
def compute_bert_similarity(text1, text2):
    # Carregar o modelo e o tokenizer
    model_name = 'neuralmind/bert-base-portuguese-cased'
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenizar os textos
    inputs1 = tokenizer(text1, return_tensors='pt', truncation=True, padding=True)
    inputs2 = tokenizer(text2, return_tensors='pt', truncation=True, padding=True)

    # Obter as embeddings
    with torch.no_grad():
        embeddings1 = model(**inputs1).last_hidden_state.mean(dim=1)
        embeddings2 = model(**inputs2).last_hidden_state.mean(dim=1)

    # Calcular a similaridade cosseno
    similarity = F.cosine_similarity(embeddings1, embeddings2)

    return similarity.item()

import spacy
#
# Verifica a simililaridade entre dois textos utilizando spacy (BERT)
#
def compute_spacy_similarity(text1, text2):
    # Carregando modelo Spacy
    nlp = spacy.load('pt_core_news_lg')
    
    # Processando textos
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    
    # Calculando Similaridade
    similarity = doc1.similarity(doc2)
    
    return similarity

####################################################################
############################### Main ###############################
####################################################################
async def main():
    path_files = "../data/step3_truncated_news"
    list_text_file = get_text_files(path_files)
    
    for text_file in list_text_file:
        print("====== Calculando e salvando os resultados ======")
        original_file = f"{os.path.splitext(os.path.basename(text_file))[0]}.txt"
        original_text = get_text_file(path_files + "/" + original_file)

        ### Whisper
        whisper_file = f"../data/result_whisper/{original_file}"
        whisper_time_file = f"../data/result_whisper/time_{original_file}"

        recognation_text = get_text_file(whisper_file)
        recognation_time = float(get_text_file(whisper_time_file).split(' ')[1])
    
        similarity = compute_cosine_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Whisper - Cosseno - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = jaccard_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Whisper - Jaccard - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = compute_spacy_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Whisper - Spacy - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = compute_bert_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Whisper - BERT - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        
        ### Google Speech Recognition
        speechRecognition_file = f"../data/result_speechRecognition/{original_file}"
        speechRecognition_time_file = f"../data/result_speechRecognition/time_{original_file}"

        recognation_text = get_text_file(speechRecognition_file)
        recognation_time = float(get_text_file(speechRecognition_time_file).split(' ')[1])

        similarity = compute_cosine_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Google_Speech_Recognition - Cosseno - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = jaccard_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Google_Speech_Recognition - Jaccard - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = compute_spacy_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Google_Speech_Recognition - Spacy - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = compute_bert_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Google_Speech_Recognition - BERT - {similarity:.2f} - {recognation_time:.4f} - {original_file}")

        ### Assemblyai
        assemblyai_file = f"../data/result_assemblyai/{original_file}"
        assemblyai_time_file = f"../data/result_assemblyai/time_{original_file}"

        recognation_text = get_text_file(assemblyai_file)
        recognation_time = float(get_text_file(assemblyai_time_file).split(' ')[1])

        similarity = compute_cosine_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Assemblyai - Cosseno - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = jaccard_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Assemblyai - Jaccard - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = compute_spacy_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Assemblyai - Spacy - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        similarity = compute_bert_similarity(original_text, recognation_text)*100
        output_append( '../data/similarity_results/', 'results.txt', f"Assemblyai - BERT - {similarity:.2f} - {recognation_time:.4f} - {original_file}")
        
        print("====== Fim do calculo e registros dos resultados ======")
asyncio.run(main())
####################################################################
####################################################################
####################################################################