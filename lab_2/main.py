"""
Lab 2
Language classification
"""
import math

from lab_1.main import tokenize, remove_stop_words
from math import dist


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
    for word in tokens:
        if not isinstance(word, str):
            return None
        freq_dict[word] = freq_dict.get(word, 0) + 1
    # convert the values in freq_dict to tokens frequency divided by the total number of tokens
    for word in freq_dict:
        freq_dict[word] = round(freq_dict[word] / len(tokens), 5)
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
    for element in texts_corpus:
        if not isinstance(element, list):
            return None
    for element in language_labels:
        if not isinstance(element, str):
            return None
    # use function get_freq_dict for EVERY list in texts_corpus via list comprehension
    new_texts_corpus = [get_freq_dict(element) for element in texts_corpus]
    language_profiles = dict(zip(language_labels, new_texts_corpus))
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    # return freq_dict keys from language_profiles as lists of unique words
    # put lists of unique words to main list "language_features"
    language_features = []
    for freq_dict in language_profiles.values():
        language_features.append(freq_dict.keys())
    if not language_features:
        return None
    # convert lists of unique words to sets and unite them
    language_features = set().union(*language_features)
    # sort in alphabetically order and return
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
    for element in original_text:
        if not isinstance(element, str):
            return None
    # unite freq_dicts from language_profiles via creating new dict
    main_freq_dict = {}
    for freq_dict in language_profiles.values():
        for key, val in freq_dict.items():
            # write the key with the highest value to the dictionary
            if val > main_freq_dict.get(key, 0):
                main_freq_dict[key] = val
                # e.g. main_freq_dict = {'a': 1,'b': 3,'c': 1}
    # use function get_language_features
    language_features = get_language_features(language_profiles)
    text_vector = []
    for word in language_features:
        if word in original_text:
            text_vector.append(main_freq_dict[word])
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
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vector, list)):
        return None
    for element in unknown_text_vector:
        if not isinstance(element, int) and not isinstance(element, float):
            return None
    for element in known_text_vector:
        if not isinstance(element, int) and not isinstance(element, float):
            return None
    # math.dist returns the Euclidean distance between two points a and b
    # roughly equivalent to: sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    distance = math.dist(unknown_text_vector, known_text_vector)
    return round(distance, 5)


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
