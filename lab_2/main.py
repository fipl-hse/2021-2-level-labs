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

    if not isinstance(tokens, list):
        return None

    freq_dict = {}
    for word in tokens:
        if isinstance(word, str):
            freq_dict[word] = round(tokens.count(word)/len(tokens), 5)
        else:
            return None
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
    for label in language_labels:
        if not label:
            return None
    for label in texts_corpus:
        if not label:
            return None

    language_profiles = {}
    for i, label in enumerate(language_labels):
        language_profiles[language_labels[i]] = get_freq_dict(texts_corpus[i])
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if not isinstance(language_profiles, dict) or not language_profiles:
        return None

    features = []
    for lang_profile in language_profiles.values():
        for word in lang_profile.keys():
            features.append(word)
    return sorted(features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if not isinstance(original_text, list) or not isinstance(language_profiles, dict) \
            or not language_profiles:
        return None

    features = get_language_features(language_profiles)
    vector_list = []
    for word in features:
        if word in original_text:
            for lang_profile in language_profiles.values():
                if word in lang_profile.keys():
                    vector_list.append(lang_profile[word])
        else:
            vector_list.append(0)
    return vector_list


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """

    if not isinstance(unknown_text_vector, list) or not \
            isinstance(known_text_vector, list):
        return None
    for i in unknown_text_vector:
        if not isinstance(i, (int, float)):
            return None
    for i in known_text_vector:
        if not isinstance(i, (int, float)):
            return None

    distance = 0
    for number, i in enumerate(unknown_text_vector):
        distance += (unknown_text_vector[number] - known_text_vector[number])**2
    return round(math.sqrt(distance), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or len(known_text_vectors) != len(language_labels):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, (int, float)):
            return None
    for vector in known_text_vectors:
        if not isinstance(vector, list):
            return None
    for label in language_labels:
        if not isinstance(label, str):
            return None

    distances = {}
    for vector, i in enumerate(known_text_vectors):
        distances[language_labels[vector]] = \
            calculate_distance(unknown_text_vector, known_text_vectors[vector])
    for key, value in distances.items():
        if value == min(distances.values()):
            nearest_language = [key, value]
    return nearest_language


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
    for i in unknown_text_vector:
        if not isinstance(i, (int, float)):
            return None
    for i in known_text_vector:
        if not isinstance(i, (int, float)):
            return None

    distance = 0
    for i, number in enumerate(unknown_text_vector):
        distance += abs(unknown_text_vector[i] - known_text_vector[i])
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

    if not isinstance(unknown_text_vector, list) \
        or not isinstance(known_text_vectors, list) \
        or not isinstance(language_labels, list)\
        or len(known_text_vectors) != len(language_labels):
        return None
    for i in unknown_text_vector:
        if not isinstance(i, (int, float)):
            return None
    for vector in known_text_vectors:
        if not isinstance(vector, list):
            return None
    for label in language_labels:
        if not isinstance(label, str):
            return None

    distances = []
    for vector in known_text_vectors:
        if metric == 'euclid':
            distances.append(calculate_distance(unknown_text_vector, vector))
        elif metric == 'manhattan':
            distances.append(calculate_distance_manhattan(unknown_text_vector, vector))

    knn_distances = sorted(distances)[:k]
    knn_language = [language_labels[distances.index(distance)] for distance in knn_distances]

    predict_language = {}
    for language in knn_language:
        if language not in predict_language:
            predict_language[language] = 0
        predict_language[language] += 1

    predict_language = max(predict_language, key=predict_language.get)
    return [predict_language, knn_distances[0]]


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
