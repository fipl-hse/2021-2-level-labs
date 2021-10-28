"""
Lab 2
Language classification
"""

from math import sqrt
from lab_1.main import tokenize, remove_stop_words


# 4
def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    freq_dict = {}
    length = len(tokens)
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    for token in freq_dict:
        freq_dict[token] = round(freq_dict[token]/length, 5)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not isinstance(texts_corpus, list) or not isinstance(language_labels, list):
        return None
    language_profiles = {}
    for label, text in zip(language_labels, texts_corpus):
        if not isinstance(label, str) or not isinstance(text, list):
            return None
        language_profiles[label] = get_freq_dict(text)
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) or len(language_profiles) == 0:
        return None
    features = []
    for freq_dict in language_profiles.values():
        if not isinstance(freq_dict, dict):
            return None
        for word in freq_dict.keys():
            if not isinstance(word, str):
                return None
            features.append(word)
    return sorted(features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or not isinstance(language_profiles, dict):
        return None
    text_vector = []
    features = get_language_features(language_profiles)
    for word in features:
        if word in original_text:
            for freq_dict in language_profiles.values():
                for key, value in freq_dict.items():
                    if key == word:
                        text_vector.append(value)
        else:
            text_vector.append(0)
    return text_vector


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    distance = 0
    for unknown_vector, known_vector in zip(unknown_text_vector, known_text_vector):
        if not isinstance(unknown_vector, (int, float)) or not isinstance(known_vector, (int, float)):
            return None
        distance += (unknown_vector - known_vector) ** 2
    return round(sqrt(distance), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not len(language_labels) == len(known_text_vectors):
        return None
    distances = []
    for known_text_vector in known_text_vectors:
        if not isinstance(known_text_vector, list) or not isinstance(unknown_text_vector, list):
            return None
        distance = calculate_distance(unknown_text_vector, known_text_vector)
        distances.append(distance)
    prediction = [language_labels[distances.index(min(distances))], min(distances)]
    return prediction


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    distance = 0
    for unknown_vector, known_vector in zip(unknown_text_vector, known_text_vector):
        if not isinstance(unknown_vector, (int, float)) or not isinstance(unknown_vector, (int, float)):
            return None
        distance += abs(unknown_vector - known_vector)
    return round(distance, 5)


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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not isinstance(k, int) or not isinstance(metric, str):
        return None
    if not len(language_labels) == len(known_text_vectors):
        return None
    distances = []
    for known_text_vector in known_text_vectors:
        if metric == 'manhattan':
            distances.append(calculate_distance_manhattan(unknown_text_vector, known_text_vector))
        elif metric == 'euclid':
            distances.append(calculate_distance(unknown_text_vector, known_text_vector))
    sorted_labels_distances = sorted(list(zip(language_labels, distances)))[:k]
    freq_labels = {}
    for label, distance in sorted_labels_distances:
        if label not in freq_labels:
            freq_labels[label] = 1
        else:
            freq_labels[label] += 1
    predicted = [max(freq_labels, key=freq_labels.get), min(distances)]
    return predicted


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
