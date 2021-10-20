"""
Lab 2
Language classification
"""

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

    for token in tokens:
        if not isinstance(token, str):
            return None

    freq_dict = {}
    tokens_len = len(tokens)

    for token in tokens:
        if token not in freq_dict:
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1

    for token in freq_dict:
        freq_dict[token] = round(freq_dict[token] / tokens_len, 5)

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
        if not isinstance(label, str):
            return None

    for text_corpus in texts_corpus:
        if not isinstance(text_corpus, list):
            return None

    language_profiles = {}

    labels_counter = 0

    for text_corpus in texts_corpus:
        language_profiles[language_labels[labels_counter]] = get_freq_dict(text_corpus)
        labels_counter += 1

    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) or language_profiles == {}:
        return None

    features = []

    for freq_dict in language_profiles.values():
        for key in freq_dict:
            features.append(key)

    return sorted(features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or not isinstance(language_profiles, dict):
        return None

    vector = []

    for unique_word in get_language_features(language_profiles):
        if unique_word in original_text:
            for freq_dict in language_profiles.values():
                if unique_word in freq_dict.keys():
                    vector.append(freq_dict[unique_word])
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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    for num in unknown_text_vector:
        if not isinstance(num, int) and not isinstance(num, float):
            return None
    for num in known_text_vector:
        if not isinstance(num, int) and not isinstance(num, float):
            return None

    distance_counter = 0
    unknown_len = len(unknown_text_vector)

    for num in range(unknown_len):
        distance_counter += ((unknown_text_vector[num])-(known_text_vector[num]))**2

    return round(distance_counter**0.5, 5)


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
    for num in unknown_text_vector:
        if not isinstance(num, int) and not isinstance(num, float):
            return None
    for num in known_text_vectors:
        if not isinstance(num, int) and not isinstance(num, float):
            return None
    for label in language_labels:
        if not isinstance(label, str):
            return None

    predict_language = []
    predict_language_dict = {}
    known_vectors_len = len(known_text_vectors)

    for num in range(known_vectors_len):
        predict_language_dict[language_labels[num]] = calculate_distance(unknown_text_vector, known_text_vectors[num])

    min_num = min(predict_language_dict.values())

    for k, v in predict_language_dict.items():
        if v == min_num:
            predict_language.append(k)
            predict_language.append(v)
    return predict_language


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
