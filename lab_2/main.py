"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words
from math import sqrt


# 4
def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not (isinstance(tokens, list)
            and all(isinstance(s, str) for s in tokens)):
        return None
    freq_dict = {}
    for i in tokens:
        freq_dict[i] = round(tokens.count(i) / len(tokens), 5)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(texts_corpus, list)
            and all(isinstance(i, list) for i in texts_corpus)
            and isinstance(language_labels, list)
            and all(isinstance(i, str) for i in language_labels)):
        return None
    language_profiles = {}
    for i, n in enumerate(language_labels):
        language_profiles[n] = get_freq_dict(texts_corpus[i])
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(language_profiles, dict) and language_profiles != {}
            and all(isinstance(i, str) for i in language_profiles)
            and all(isinstance(i, dict) for i in language_profiles.values())):
        return None
    features = [i for n in language_profiles.values() for i in n if all(n)]
    features.sort()
    return features


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(original_text, list) and language_profiles != {}
            and all(isinstance(i, str) for i in original_text)
            and isinstance(language_profiles, dict)
            and all(isinstance(i, dict) for i in language_profiles.values())):
        return None
    features = get_language_features(language_profiles)
    vector_freq_dict = dict.fromkeys(features, 0)
    for word in features:
        if word not in original_text:
            continue
        for freq_dict in language_profiles.values():
            for key, value in freq_dict.items():
                if key != word:
                    continue
                if value <= vector_freq_dict[key]:
                    continue
                vector_freq_dict[key] = value
    text_vector = list(vector_freq_dict.values())
    return text_vector


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(s, (float, int)) for s in unknown_text_vector)
            and isinstance(known_text_vector, list)
            and all(isinstance(t, (float, int)) for t in known_text_vector)):
        return None
    distance = 0
    for i, n in zip(unknown_text_vector, known_text_vector):
        distance += (i - n) ** 2
    distance = round(sqrt(distance), 5)
    return distance


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(s, (float, int)) for s in unknown_text_vector)
            and isinstance(known_text_vectors, list)
            and all(isinstance(t, list) for t in known_text_vectors)
            and isinstance(language_labels, list)
            and all(isinstance(f, str) for f in language_labels)
            and len(known_text_vectors) == len(language_labels)):
        return None
    list_of_scores = [[] for i in range(len(known_text_vectors))]
    k = 0
    while True:
        if k == len(known_text_vectors):
            break
        distance = calculate_distance(unknown_text_vector, known_text_vectors[k])
        list_of_scores[k].append(distance)
        list_of_scores[k].append(language_labels[k])
        k += 1
    list_of_scores.sort()
    list_of_scores[0][0], list_of_scores[0][1] = list_of_scores[0][1], list_of_scores[0][0]
    return list_of_scores[0]


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(s, (float, int)) for s in unknown_text_vector)
            and isinstance(known_text_vector, list)
            and all(isinstance(t, (float, int)) for t in known_text_vector)):
        return None
    distance = 0
    for i, n in zip(unknown_text_vector, known_text_vector):
        distance += abs(i - n)
    distance = round(distance, 5)
    return distance


def predict_language_knn(unknown_text_vector: list, known_text_vectors: list,
                         language_labels: list, k=1, metric='manhattan') -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
        using knn based algorithm and specific metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    :param k: the number of neighbors to choose label from
    :param metric: specific metric to use while calculating distance
    """
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(i, (int, float)) for i in unknown_text_vector)
            and isinstance(known_text_vectors, list)
            and all(isinstance(n, list) for n in known_text_vectors)
            and isinstance(language_labels, list)
            and all(isinstance(s, str) for s in language_labels)
            and len(known_text_vectors) == len(language_labels)):
        return None
    list_of_scores = [[] for i in range(len(known_text_vectors))]
    list_knn = []
    list_newest = []
    dict_counter = {}
    m = 0
    distance = 0
    while True:
        if m == len(known_text_vectors):
            break
        if metric == 'euclid':
            distance = calculate_distance(unknown_text_vector, known_text_vectors[m])
        if metric == 'manhattan':
            distance = calculate_distance_manhattan(unknown_text_vector, known_text_vectors[m])
        list_of_scores[m].append(distance)
        list_of_scores[m].append(language_labels[m])
        m += 1
    list_of_scores.sort()
    f = k
    while f != -1:
        list_of_scores[f][0], list_of_scores[f][1] = list_of_scores[f][1], list_of_scores[f][0]
        f -= 1
    for i in list_of_scores[:k]:
        list_knn.append(i[0])
    for i in list_knn:
        dict_counter[i] = list_knn.count(i)
    right_label = sorted(dict_counter, key=dict_counter.get, reverse=True)[0]
    list_newest.extend([right_label, list_of_scores[0][1]])
    return list_newest


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    pass


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    pass


def predict_language_knn_sparse(unknown_text_vector: list, known_text_vectors: list,
                                language_labels: list, k=1) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
        using knn based algorithm
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vectors: a list of sparse vectors for known texts
    :param language_labels: language labels for each known text
    :param k: the number of neighbors to choose label from
    """
    pass
