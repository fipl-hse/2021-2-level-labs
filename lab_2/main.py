"""
Lab 2
Language classification
"""

import math
from lab_1.main import tokenize, remove_stop_words


# 4
def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if not isinstance(tokens, list) or not all(isinstance(i, str) for i in tokens):
        return None
    freq_dict = {}
    for i in tokens:
        if i in freq_dict:
            freq_dict[i] += 1/len(tokens)
        else:
            freq_dict[i] = 1/len(tokens)
    for i in freq_dict:
        freq_dict[i] = round(freq_dict[i], 5)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """

    if (not isinstance(texts_corpus, list) or
            not isinstance(language_labels, list) or not all(isinstance(i, list) for i in texts_corpus) or
            not all(isinstance(i, str) for i in language_labels)):
        return None
    lang_pr = {}
    for i in range(len(texts_corpus)):
        lang_pr[language_labels[i]] = get_freq_dict(texts_corpus[i])
    return lang_pr


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if (not isinstance(language_profiles, dict) or
            not all(isinstance(key, str) for key in language_profiles.keys()) or
            not all(isinstance(value, dict) for value in language_profiles.values()) or
            not language_profiles.items()):
        return None
    features = []
    for i in language_profiles.values():
        for word in i:
            if word not in features:
                features.append(word)
    return sorted(features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if (not isinstance(original_text, list) or
            not isinstance(language_profiles, dict) or
            not all(isinstance(key, str) for key in language_profiles.keys()) or
            not all(isinstance(value, dict) for value in language_profiles.values()) or
            not language_profiles.items()):
        return None
    unique_words = get_language_features(language_profiles)
    text_vector = []
    for i in unique_words:
        freq_list = []
        if i in original_text:
            for lang in language_profiles.values():
                if i in lang:
                    freq_list.append(lang.get(i))
        else:
            freq_list.append(0)
        text_vector.append(sorted(freq_list)[0])
    return text_vector


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """

    if (not isinstance(unknown_text_vector, list) or
            not isinstance(known_text_vector, list) or
            not all(isinstance(i, (float, int)) for i in unknown_text_vector) or
            not all(isinstance(i, (float, int)) for i in known_text_vector)):
        return None
    sq_dif = []
    for i in range(len(unknown_text_vector)):
        sq_dif.append((unknown_text_vector[i] - known_text_vector[i])**2)
    return round(math.sqrt(sum(sq_dif)), 5)


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
