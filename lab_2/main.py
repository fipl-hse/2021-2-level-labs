"""
Lab 2
Language classification
"""
import math

from lab_1.main import tokenize, remove_stop_words


# 4
def get_freq_dict(tokens):
    if not isinstance(tokens, list):
        return None
    frequency_dict = {}
    for word in tokens:
        if not isinstance(word, str):
            return None
        if word in frequency_dict:
            frequency_dict[word] += 1 / len(tokens)
        else:
            frequency_dict[word] = 1 / len(tokens)
    for key, value in frequency_dict.items():
        value = round(value, 5)
        frequency_dict[key] = value
    return frequency_dict

def get_language_profiles(texts_corpus, language_labels):
    if not (isinstance(texts_corpus, list) and isinstance(language_labels, list)):
        return None
    for label in language_labels:
        if not isinstance(label, str):
            return None
    language_profiles = {}
    for index, label in enumerate(language_labels):
        language_profiles[label] = get_freq_dict(texts_corpus[index])
    return language_profiles

def get_language_features(language_profiles):
    if not (isinstance(language_profiles, dict) and language_profiles):
        return None
    unique_list = []
    for frequency_dict in language_profiles.values():
        for token in frequency_dict:
            if token not in unique_list:
                unique_list.append(token)
    unique_list.sort()
    return unique_list

def get_text_vector(original_text, language_profiles):
    if not (isinstance(original_text, list) and isinstance(language_profiles, dict)
            and original_text and language_profiles):
        return None
    text_vector = []
    unique_words = get_language_features(language_profiles)
    for word in unique_words:
        if word not in original_text:
            text_vector.append(0)
        else:
            for profile in language_profiles.values():
                if word in profile.keys():
                    text_vector.append(profile[word])
    return text_vector

# 6
def calculate_distance(unknown_text_vector, known_text_vector):
    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vector, list) and unknown_text_vector
            and known_text_vector):
        return None
    for number in unknown_text_vector:
        if not (isinstance(number, int) or isinstance(number, float)):
            return None
    for number in known_text_vector:
        if not (isinstance(number, int) or isinstance(number, float)):
            return None
    distance_btw_vectors = 0
    for number in range(len(unknown_text_vector)):
        distance_btw_vectors += (unknown_text_vector[number]-known_text_vector[number]) ** 2
    distance_btw_vectors = round(math.sqrt(distance_btw_vectors), 5)
    return distance_btw_vectors

def predict_language_score(unknown_text_vector, known_text_vectors, language_labels):
    if not (isinstance(unknown_text_vector, list) or isinstance(known_text_vectors, list)
            or isinstance(language_labels, list) or len(language_labels) == len(known_text_vectors)):
        return None
    dist_list = []
    min_dist = []
    for known_text_vector in known_text_vectors:
        if not isinstance(known_text_vector, list):
            return None
        dist_list.append(calculate_distance(unknown_text_vector, known_text_vector))
    min_dist_v = min(dist_list)
    min_dist.extend([language_labels[dist_list.index(min_dist_v)], min_dist_v])
    return min_dist

# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    pass


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
    pass


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
