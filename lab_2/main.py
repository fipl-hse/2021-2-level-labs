"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words
from math import sqrt


def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    for token in tokens:
        if not isinstance(token, str):
            return None

    freqs = {}
    full_length = len(tokens)
    for word in tokens:
        if word not in freqs.keys():
            freqs[word] = 1
        else:
            freqs[word] += 1

    freqs.update((x, round(y / full_length, ndigits=5)) for x, y in freqs.items())

    return freqs


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """

    if not isinstance(texts_corpus, list):
        return None
    if not isinstance(language_labels, list):
        return None
    for label in language_labels:
        if not isinstance(label, str):
            return None

    language_profiles = {}

    for i, label in enumerate(language_labels):
        language_profiles[label] = get_freq_dict(texts_corpus[i])

    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    if language_profiles == {}:
        return None
    for profile_name, profile in language_profiles.items():
        if not isinstance(profile_name, str):
            return None
        if not isinstance(profile, dict):
            return None

    unique = []

    for profile_full in language_profiles.values():
        for profile_word in profile_full.keys():
            if profile_word not in unique:
                unique.append(profile_word)

    return sorted(unique)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list):
        return None
    if not isinstance(language_profiles, dict):
        return None
    if language_profiles == {}:
        return None

    text_vector = []
    unique_words = get_language_features(language_profiles)

    for word in unique_words:
        if word in original_text:
            for profile in language_profiles.values():
                if word in profile.keys():
                    text_vector.append(profile[word])
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
    if not isinstance(unknown_text_vector, list):
        return None
    for element in unknown_text_vector:
        if element is None:
            return None

    if not isinstance(known_text_vector, list):
        return None
    for element in known_text_vector:
        if element is None:
            return None

    distance = 0
    for unknown, known in zip(unknown_text_vector, known_text_vector):
        distance += (unknown - known) ** 2

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
    pass


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
