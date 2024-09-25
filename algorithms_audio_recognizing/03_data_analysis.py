import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from output_recognizer import output_append

#
# Ler e trata os resultados gerados a partir das transcrições
#
def read_results_file(filename):
    methods = set()
    similarity_measures = set()
    data = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) >= 3:
                method = parts[0]
                similarity_measure = parts[1]
                score = float(parts[2])
                time = float(parts[3])
                file_name = parts[4]
                
                methods.add(method)
                similarity_measures.add(similarity_measure)
                data.append((method, similarity_measure, score, time, file_name))
    
    return methods, similarity_measures, data

def plot_similarity_scores(methods, similarity_measures, data):
    methods = sorted(methods)
    similarity_measures = sorted(similarity_measures)

    # Preparando dados para plotting
    scores = {method: [0] * len(similarity_measures) for method in methods}
    
    for method, measure, score, time, file_name in data:
        if method in scores and measure in similarity_measures:
            index = similarity_measures.index(measure)
            scores[method][index] = score
    
    x = np.arange(len(similarity_measures))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Definindo cores para cada método
    colors = {
        'Whisper': '#1f77b4',  # azul
        'Google_Speech_Recognition': '#2ca02c',  # verde
        'Assemblyai': '#d62728'  # vermelho
    }

    for i, method in enumerate(methods):
        ax.bar(x + i * width, scores[method], width, label=method, color=colors.get(method))
    
    ax.set_xlabel('Métodos de Similaridade', fontweight='bold')
    ax.set_ylabel('Percentual (%)', fontweight='bold')
    plt.yticks(np.arange(0, 101, 10)) # Definindo ticks do eixo Y de 10 em 10
    ax.set_title('Gráficos do Percentual de Similaridade', fontweight='bold')
    ax.set_xticks(x + width * (len(methods) - 1) / 2)
    ax.set_xticklabels(similarity_measures, rotation=0, ha='center')
    ax.legend(title='Ferramentas', loc=(0.77, -0.18))  # Alterando a posição da legenda

    plt.tight_layout()
    plt.savefig('../data/similarity_results/Grafico_Porcentagens.png')

def plot_average_times(data):
    time_data = {}

    # Processando os dados
    for method, measure, score, time, file_name in data:
        if method not in time_data:
            time_data[method] = []
        time_data[method].append(time)

    # Calculando a média dos tempos
    average_times = {method: np.mean(times) for method, times in time_data.items()}

    # Separando os dados para o gráfico
    methods = list(average_times.keys())
    values = list(average_times.values())

    # Criando o gráfico de barras
    plt.figure(figsize=(12, 6))
    bars = plt.bar(methods, values, color='pink', zorder=2)
    
    # Adicionando linhas horizontais a cada 2 segundos
    max_value = int(max(values)) + 2  # Ajuste para incluir a última linha
    for y in range(0, max_value + 1, 2):
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.7, zorder=1)

    plt.xlabel('Métodos de Similaridade', fontweight='bold')
    plt.ylabel('Tempo Médio (segundos)', fontweight='bold')
    plt.yticks(np.arange(0, 37, 4)) # Definindo ticks do eixo Y de 4 em 4
    plt.title('Tempo Médio por Método de Similaridade', fontweight='bold')
    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    plt.savefig('../data/similarity_results/Grafico_Tempo_Medio.png')

def plot_boxplot(data):
    # Convertendo os dados para um DataFrame
    df = pd.DataFrame(data, columns=['method', 'similarity_seasure', 'score', 'time', 'file_name'])

    # Criando o gráfico box plot
    plt.figure(figsize=(12, 6))
    boxplot = df.boxplot(column='time', by='method', grid=False)

    plt.title('Box Plot do Tempo por Método de Similaridade', fontweight='bold')
    plt.suptitle('')  # Remove o título padrão gerado pelo boxplot
    plt.xlabel('Métodos de Similaridade', fontweight='bold')
    plt.ylabel('Tempo (segundos)', fontweight='bold')

    plt.ylim(0, 36)
    # Definindo ticks do eixo Y de 5 em 5
    plt.yticks(range(0, 81, 5))

    plt.tight_layout()
    plt.savefig('../data/similarity_results/Grafico_Boxplot_Tempos.png')

"""
def plot_scatter_times(data):
    # Inicializando um dicionário para armazenar os tempos
    time_data = {}

    # Processando os dados
    for method, measure, score, time, file_name in data:
        if method not in time_data:
            time_data[method] = []
        time_data[method].append(time)

    # Separando os dados para o gráfico
    methods = list(time_data.keys())
    all_times = [time for times in time_data.values() for time in times]
    all_methods = [method for method in methods for _ in time_data[method]]

    # Criando o gráfico de dispersão
    plt.figure(figsize=(12, 6))
    
    # Adicionando linhas horizontais a cada 2 segundos
    max_value = int(max(all_times)) + 2  # Ajuste para incluir a última linha
    for y in range(0, max_value + 1, 2):
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.7)

    # Criando o gráfico de dispersão
    plt.scatter(all_methods, all_times, color='blue', alpha=0.6)

    plt.xlabel('Métodos de Similaridade', fontweight='bold')
    plt.ylabel('Tempo (segundos)', fontweight='bold')  # Rótulo em negrito
    plt.title('Dispersão do Tempo por Método de Similaridade', fontweight='bold')
    
    # Ajustando o limite do eixo Y para ir até 36
    plt.ylim(0, 36)

    # Definindo ticks do eixo Y de 4 em 4
    plt.yticks(np.arange(0, 37, 4))

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('../data/similarity_results/dispersao_tempos.png')
    plt.show()
"""

#
# Obtém o maior e o menor tempo para cada método de similaridade.
# Retorna: Um dicionário com o método como chave e uma tupla (menor_tempo, maior_tempo) como valor.
#
def get_max_min_times(data):
    time_data = {}

    for method, measure, score, time, file_name in data:
        if method not in time_data:
            time_data[method] = []
        time_data[method].append((time, file_name))

    # Calculando o menor e o maior tempo para cada método
    min_max_times = {}
    for method, times in time_data.items():
        min_time, min_file = min(times, key=lambda x: x[0])
        max_time, max_file = max(times, key=lambda x: x[0])
        min_max_times[method] = (min_time, min_file, max_time, max_file)

    return min_max_times

#
# Obtém o maior e o menor percentual (score) para cada método de similaridade, incluindo os nomes dos arquivos.
# Retorna: Um dicionário com o método como chave e uma tupla (menor_score, file_name_menor, maior_score, file_name_maior) como valor.
#
def get_max_min_scores(data):
    score_data = {}

    for method, measure, score, time, file_name in data:
        if method not in score_data:
            score_data[method] = []
        score_data[method].append((score, file_name))

    # Calculando o menor e o maior score para cada método
    min_max_scores = {}
    for method, scores in score_data.items():
        min_score, min_file = min(scores, key=lambda x: x[0])
        max_score, max_file = max(scores, key=lambda x: x[0])
        min_max_scores[method] = (min_score, min_file, max_score, max_file)

    return min_max_scores

####################################################################
############################### Main ###############################
####################################################################
filename = '../data/similarity_results/results.txt'
methods, similarity_measures, data = read_results_file(filename)
plot_similarity_scores(methods, similarity_measures, data)
plot_average_times(data)
plot_boxplot(data)
#plot_scatter_times(data)

max_min_times = get_max_min_times(data)
max_min_scores = get_max_min_scores(data)
for method in max_min_times:
    output_append( '../data/similarity_results/', 'results_values.txt', f"{method}: Tempo Min {max_min_times.get(method)[0]} s - {max_min_times.get(method)[1]}")
    output_append( '../data/similarity_results/', 'results_values.txt', f"{method}: Tempo Max {max_min_times.get(method)[2]} s - {max_min_times.get(method)[3]}")
    output_append( '../data/similarity_results/', 'results_values.txt', f"{method}: Percentual Min {max_min_scores.get(method)[0]}% - {max_min_scores.get(method)[1]}")
    output_append( '../data/similarity_results/', 'results_values.txt', f"{method}: Percentual Max {max_min_scores.get(method)[2]}% - {max_min_scores.get(method)[3]}")