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

    freq = {}
    all_words = len(tokens)

    for token in tokens:
        if not isinstance(token, str):
            return None
        else:
            freq[token] = round(tokens.count(token) / all_words, 5)
    return freq


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """

    if not (isinstance(texts_corpus, list) and isinstance(language_labels, list)):
        return None

    for language in language_labels:
        for text in texts_corpus:
            if not language:
                return None
            if not text:
                return None

    language_profiles = {}

    for language in range(len(language_labels)):
        language_profiles[language_labels[language]] = get_freq_dict(texts_corpus[language])
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

    for language in language_profiles.values():
        for key in language.keys():
            features.append(key)
    return sorted(features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if not (isinstance(original_text, list) and isinstance(language_profiles, dict)) or not language_profiles:
        return None

    features = get_language_features(language_profiles)
    vector = []

    for word in features:
        if word in original_text:
            for value in language_profiles.values():
                if word in value.keys():
                    vector.append(value[word])
        else:
            vector.append(0)
    return vector


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """

    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vector, list)):
        return None

    for num in unknown_text_vector:
        if not (isinstance(num, (int, float))):
            return None
    for num in known_text_vector:
        if not (isinstance(num, (int, float))):
            return None

    dist = 0
    counter = 0

    for index, number in enumerate(unknown_text_vector):
        if counter < len(known_text_vector):
            dist += ((number - known_text_vector[index])**2)
            counter += 1
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

    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vectors, list)
            and isinstance(language_labels, list)) or len(language_labels) != len(known_text_vectors):
        return None

    for num in unknown_text_vector:
        if not isinstance(num, (int, float)):
            return None
    for vector in known_text_vectors:
        if not isinstance(vector, list):
            return None
    for language in language_labels:
        if not isinstance(language, str):
            return None

    comp = {}

    for vector in range(len(known_text_vectors)):
        comp[language_labels[vector]] = calculate_distance(unknown_text_vector, known_text_vectors[vector])

    for key, value in comp.items():
        if value == min(comp.values()):
            result = [key, value]
    return result
