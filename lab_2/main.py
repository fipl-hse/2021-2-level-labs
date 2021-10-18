"""
Lab 2
Language classification
"""

from itertools import zip_longest
from math import sqrt

from lab_1.main import tokenize, remove_stop_words


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

    # changing the values of the keys from raw frequencies to freq / all elements
    # resulting in asked value
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

    for index, label in enumerate(language_labels):
        language_profiles[label] = get_freq_dict(texts_corpus[index])

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
        if not isinstance(profile_name, str) or not isinstance(profile, dict):
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

    text_vector = {}
    unique_words = get_language_features(language_profiles)
    # a dict of type unique word:0
    vector_freq = dict.fromkeys(unique_words, 0)

    # going through the unique words
    # if we can find the word and its value in profiles
    # and it's lower than the one we might've updated earlier
    # we change it to the one stored in the profile
    for word in unique_words:
        if word in original_text:
            for profile in language_profiles.values():
                for key, value in profile.items():
                    if key == word and value > vector_freq[key]:
                        vector_freq[key] = value

    # we need list of vector element so we convert values to a list
    text_vector = list(vector_freq.values())

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
    if not isinstance(unknown_text_vector, list):
        return None

    if not isinstance(known_text_vectors, list):
        return None
    for known_vector in known_text_vectors:
        if not isinstance(known_vector, list):
            return None

    if len(known_text_vectors) != len(language_labels):
        return None

    if not isinstance(language_labels, list):
        return None

    detected_language = ['', 1]
    for i, known_vector in enumerate(known_text_vectors):
        tmp = calculate_distance(unknown_text_vector, known_vector)
        if detected_language[1] > tmp:
            detected_language[1] = tmp
            detected_language[0] = language_labels[i]

    return detected_language


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
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
        distance += abs(unknown - known)

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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list):
        return None

    for known_vector in known_text_vectors:
        if not isinstance(known_vector, list):
            return None

    if len(known_text_vectors) != len(language_labels) or not isinstance(language_labels, list):
        return None

    # list of calculated distances and their tags with each pair separated
    distances = []

    if metric == "manhattan":
        for i, known_vector in enumerate(known_text_vectors):
            distances.append([language_labels[i],
                              calculate_distance_manhattan(unknown_text_vector, known_vector)])

    if metric == "euclid":
        for i, known_vector in enumerate(known_text_vectors):
            distances.append([language_labels[i],
                              calculate_distance(unknown_text_vector, known_vector)])

    # sorting by the second value (distance) lists in distance list
    distances.sort(key=lambda x: x[1])
    distances = distances[:k]

    # counting the number of each label occurring in the distances list in tmp
    tmp = {}
    for language in distances:
        if language[0] not in tmp:
            tmp[language[0]] = 1
        else:
            tmp[language[0]] += 1

    # getting the biggest value from tmp dict
    max_l_tmp = max(tmp, key=tmp.get)
    result = [max_l_tmp, distances[0][1]]

    return result


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or not isinstance(language_profiles, dict):
        return None
    for label, language in language_profiles.items():
        if not isinstance(label, str) or not isinstance(language, dict):
            return None

    unique_words = get_language_features(language_profiles)
    text_vector_sparse = []

    # going through unique tokens and their numbers
    for i, word in enumerate(unique_words):
        # if the word is in the original text then we look for it in the profiles
        # and add it in [position, frequency] format
        if word in original_text:
            for profile in language_profiles.values():
                if word in profile.keys():
                    text_vector_sparse.append([i, profile[word]])
    return text_vector_sparse


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
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

    # helps with the fact that one lists can be longer than the other
    # creates [-1, 0] if the list has ended and the other list didn't
    for unknown, known in zip_longest(unknown_text_vector, known_text_vector,
                                      fillvalue=[-1, 0]):

        if unknown[0] == known[0]:
            distance += (unknown[1] - known[1]) ** 2
        else:
            if known[0] >= 0:
                distance += known[1] ** 2
            if unknown[0] >= 0:
                distance += unknown[1] ** 2

    return round(sqrt(distance), 5)


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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list):
        return None

    for known_vector in known_text_vectors:
        if not isinstance(known_vector, list):
            return None

    if len(known_text_vectors) != len(language_labels) or not isinstance(language_labels, list):
        return None

    # list of calculated distances and their tags with each pair separated
    distances = []

    for i, known_vector in enumerate(known_text_vectors):
        distances.append([language_labels[i],
                          calculate_distance_sparse(unknown_text_vector, known_vector)])

    # sorting by the second value (distance) lists in distance list
    distances.sort(key=lambda x: x[1])
    distances = distances[:k]

    # counting the number of each label occurring in the distances list in tmp
    tmp = {}
    for language in distances:
        if language[0] not in tmp:
            tmp[language[0]] = 1
        else:
            tmp[language[0]] += 1

    # getting the biggest value from tmp dict
    max_l_tmp = max(tmp, key=tmp.get)
    result = [max_l_tmp, distances[0][1]]

    return result

