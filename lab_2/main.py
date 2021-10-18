"""
Lab 2
Language classification
"""

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

def get_language_profiles(texts_corpus, language_labels) -> dict or None:
    if not isinstance(texts_corpus, list) and isinstance(language_labels, list):
        return None
    if None in texts_corpus or None in language_labels:
        return None
    language_profiles = {}
    for label in range(len(language_labels)):
        language_profiles[language_labels[label]] = get_freq_dict(texts_corpus[label])
    return language_profiles

def get_language_features(language_profiles) -> list or None:
    if not isinstance(language_profiles, dict) or language_profiles == {}:
        return None
    unique_list = []
    for frequency_dict in language_profiles.values():
        if None in frequency_dict \
                or not isinstance(frequency_dict, dict):
            return None
        unique_list.extend(list(frequency_dict.keys()))
    unique_list = list(set(unique_list))
    unique_list = sorted(unique_list)
    return unique_list

def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    pass


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    pass


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
