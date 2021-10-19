"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words
import math

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

    for token in tokens:
        if not isinstance(token, str):
            return None
        if token not in freq_dict:
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1

    for freq in freq_dict:
        freq_dict[freq] = round(freq_dict[freq]/len(tokens), 5)
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

    for texts in texts_corpus:
        if not isinstance(texts, list):
            return None

    for label in language_labels:
        if not isinstance(label, str):
            return None

    for texts, label in zip(texts_corpus, language_labels):
        language_profiles[label] = get_freq_dict(texts)
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None

    language_features = []

    for values in language_profiles.values():
        for key in values.keys():
            if key not in language_features:
                language_features.append(key)

    for feature in language_features:
        if not isinstance(feature, str):
            return None
        return sorted(language_features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or not isinstance(language_profiles, dict):
        return None

    features = get_language_features(language_profiles)
    text_vector = dict.fromkeys(features, 0)

    for language_profile in language_profiles.values():
        for feature, value_score in language_profile.items():
            if value_score > text_vector[feature] and feature in original_text:
                text_vector[feature] = value_score
    vector = list(text_vector.values())
    return vector

# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) and isinstance(known_text_vector, list):
        return None

    for unknown_vector in unknown_text_vector:
        if not isinstance(unknown_vector, (float, int)):
            return None

    for known_vector in known_text_vector:
        if not isinstance(known_vector, (float, int)):
            return None

    dist = 0

    for index, number in enumerate(unknown_text_vector):
        dist += (number - known_text_vector[index]) ** 2
    distance = round(math.sqrt(dist), 5)
    return distance


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) or not isinstance(language_labels, list):
        return None

    if len(language_labels) != len(known_text_vectors):
        return None

    for element in unknown_text_vector:
        if not isinstance(element, (float, int)):
            return None

    lang_score = list(calculate_distance(unknown_text_vector, unknown_vector) for unknown_vector in known_text_vectors)
    return list(min(zip(language_labels, lang_score)))


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
