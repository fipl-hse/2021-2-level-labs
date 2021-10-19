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
    frequency_dictionary = {}
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token in frequency_dictionary:
            frequency_dictionary[token] += 1
        else:
            frequency_dictionary[token] = 1
    for token in frequency_dictionary:
        frequency_dictionary[token] = round(frequency_dictionary[token]/len(tokens), 5)
    return frequency_dictionary


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if (not isinstance(texts_corpus, list)
            or not isinstance(language_labels, list)):
        return None
    for elem in texts_corpus:
        if not isinstance(elem, list):
            return None
    for elem in language_labels:
        if not isinstance(elem, str):
            return None
    freq_dictionary = [get_freq_dict(elem) for elem in texts_corpus]
    language_profiles = dict(zip(language_labels, freq_dictionary))
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
    for freq_dictionary in language_profiles.values():
        language_features += freq_dictionary.keys()
    language_features.sort()
    if not language_features:
        return None
    return language_features


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if (not isinstance(original_text, list)
            or not isinstance(language_profiles, dict)):
        return None
    text_vector = []
    for language_feature in get_language_features(language_profiles):
        if language_feature in original_text:
            for freq_dictionary in language_profiles.values():
                if language_feature in freq_dictionary:
                    text_vector.append(freq_dictionary[language_feature])
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
    distance = 0
    for unknown, known in zip(unknown_text_vector, known_text_vector):
        if known is None or unknown is None:
            return None
        distance += (unknown - known)**2
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
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vectors, list)
            or not isinstance(language_labels, list)):
        return None
    if len(known_text_vectors) != len(language_labels):
        return None
    predicted_language = ['', 1]
    for language, known_text_vector in enumerate(known_text_vectors):
        if known_text_vector is None:
            return None
        distance = calculate_distance(unknown_text_vector, known_text_vector)
        if predicted_language[1] > distance:
            predicted_language[0] = language_labels[language]
            predicted_language[1] = distance
    return predicted_language


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vector, list)):
        return None
    distance = 0
    for unknown, known in zip(unknown_text_vector, known_text_vector):
        if known is None or unknown is None:
            return None
        distance += round(abs(unknown - known), 5)
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
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vectors, list)
            or not isinstance(language_labels, list)):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, (float, int)):
            return None
    distances = []
    if metric == 'manhattan':
        for known_text_vector in known_text_vectors:
            distances.append(calculate_distance_manhattan(unknown_text_vector, known_text_vector))
    if metric == 'euclid':
        for known_text_vector in known_text_vectors:
            distances.append(calculate_distance(unknown_text_vector, known_text_vector))
    nearest_languages = sorted(list(zip(language_labels, distances)))[:k]
    if not isinstance(nearest_languages, list):
        return None
    count_languages = {}
    for language in nearest_languages:
        if language not in count_languages:
            count_languages[language] = 1
        else:
            count_languages[language] += 1
    biggest_value = max(count_languages, key=count_languages.get)
    predicted_language = [biggest_value[0], round(min(distances), 5)]
    return predicted_language


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if (not isinstance(original_text, list)
            or not isinstance(language_profiles, dict)):
        return None
    text_vector = []
    for feature in get_language_features(language_profiles):
        if feature in original_text:
            for freq_dictionary in language_profiles.values():
                if feature in freq_dictionary:
                    text_vector.append([(get_language_features(language_profiles)).index(feature),
                                        freq_dictionary[feature]])
    return text_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vector, list)):
        return None
    for element in unknown_text_vector:
        if not isinstance(element, list):
            return None
    for element in known_text_vector:
        if not isinstance(element, list):
            return None
    dictionary = dict(unknown_text_vector)
    for key in known_text_vector:
        if key[0] in dictionary:
            dictionary[key[0]] -= key[1]
        else:
            dictionary[key[0]] = key[1]
    distance = 0
    for value in dictionary.values():
        distance += value ** 2
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
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vectors, list)
            or not isinstance(language_labels, list)
            or not isinstance(k, int)):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    distances = []
    for known_text_vector in known_text_vectors:
        distances.append(calculate_distance_sparse(unknown_text_vector, known_text_vector))
    nearest_languages = sorted(zip(language_labels, distances))[:k]
    count_languages = {}
    for language in nearest_languages:
        if language[0] not in count_languages:
            count_languages[language[0]] = 1
        else:
            count_languages[language[0]] += 1
    biggest_value = max(count_languages, key=count_languages.get)
    predicted_language = [biggest_value, min(distances)]
    return predicted_language
