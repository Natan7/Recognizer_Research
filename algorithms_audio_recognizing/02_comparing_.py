import os
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

from sentence_transformers import SentenceTransformer, util
#
# Verifica a simililaridade entre dois textos utilizando BERT
#
def compute_bert_similarity(text1, text2):
    # Carregando modelo pré-treino BERT
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Encode os textos
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)
    
    # Calculando Similaridade Cosseno
    similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
    
    return similarity.item()

import spacy
#
# Verifica a simililaridade entre dois textos utilizando spacy (BERT)
#
def compute_spacy_similarity(text1, text2):
    # Carregando modelo Spacy
    nlp = spacy.load('pt_core_web_md')
    
    # Processando textos
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    
    # Calculando Similaridade
    similarity = doc1.similarity(doc2)
    
    return similarity


####################################################################
############################### Main ###############################
####################################################################
path_files = "../data/step3_truncated_news"
list_text_file = get_text_files(path_files)

for text_file in list_text_file:
    original_file = os.path.splitext(os.path.basename(text_file))[0] + '.txt'
    original_text = get_text_file(path_files + "/" + original_file)

    whisper_file = "../data/result_whisper/" + original_file
    speechRecognition_file = "../data/result_speechRecognition/" + original_file
    assemblyai_file = "../data/result_assemblyai/" + original_file

    recognation_text = get_text_file(whisper_file)
    print()  
    print("======Result======")

    print("whisper")
    similarity = compute_cosine_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"whisper - Cosine_Similarity - {similarity:.4f} - {original_file}")
    similarity = jaccard_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"whisper - Jaccard_Similarity - {similarity:.4f} - {original_file}")
    similarity = compute_spacy_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"whisper - Spacy_Similarity - {similarity:.4f} - {original_file}")
    similarity = compute_bert_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"whisper - BERT_Similarity - {similarity:.4f} - {original_file}")
    print("endddd")

    print("speechRecognition_file")
    recognation_text = get_text_file(speechRecognition_file)
    similarity = compute_cosine_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"speechRecognition - Cosine_Similarity - {similarity:.4f} - {original_file}")
    similarity = jaccard_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"speechRecognition - Jaccard_Similarity - {similarity:.4f} - {original_file}")
    similarity = compute_spacy_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"speechRecognition - Spacy_Similarity - {similarity:.4f} - {original_file}")
    similarity = compute_bert_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"speechRecognition - BERT_Similarity - {similarity:.4f} - {original_file}")
    print("endddd")


    print("assemblyai")
    recognation_text = get_text_file(assemblyai_file)
    similarity = compute_cosine_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"assemblyai - Cosine_Similarity - {similarity:.4f} - {original_file}")
    similarity = jaccard_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"assemblyai - Jaccard_Similarity - {similarity:.4f} - {original_file}")
    similarity = compute_spacy_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"assemblyai - Spacy_Similarity - {similarity:.4f} - {original_file}")
    similarity = compute_bert_similarity(original_text, recognation_text)
    output_append( '../data/similarity_results/', 'results.txt', f"assemblyai - BERT_Similarity - {similarity:.4f} - {original_file}")
    print("endddd")

####################################################################
####################################################################
####################################################################