import matplotlib.pyplot as plt
import numpy as np

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
                
                methods.add(method)
                similarity_measures.add(similarity_measure)
                data.append((method, similarity_measure, score))
    
    return methods, similarity_measures, data

def plot_similarity_scores(methods, similarity_measures, data):
    methods = sorted(methods)
    similarity_measures = sorted(similarity_measures)

    # Prepare data for plotting
    scores = {method: [0] * len(similarity_measures) for method in methods}
    
    for method, measure, score in data:
        if method in scores and measure in similarity_measures:
            index = similarity_measures.index(measure)
            scores[method][index] = score
    
    x = np.arange(len(similarity_measures))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 8))

    for i, method in enumerate(methods):
        ax.bar(x + i * width, scores[method], width, label=method)

    ax.set_xlabel('Similarity Measures')
    ax.set_ylabel('Scores')
    ax.set_title('Similarity Scores by Method and Measure')
    ax.set_xticks(x + width * (len(methods) - 1) / 2)
    ax.set_xticklabels(similarity_measures, rotation=45, ha='right')
    ax.legend(title='Method')

    plt.tight_layout()
    plt.show()

####################################################################
############################### Main ###############################
####################################################################
filename = '../data/similarity_results/results.txt'
methods, similarity_measures, data = read_results_file(filename)
plot_similarity_scores(methods, similarity_measures, data)
