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
        if not token:
            return None

    freq_dict = {}
    for token in tokens:
        freq_dict[token] = round(tokens.count(token)/len(tokens), 5)
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
    for text in texts_corpus:
        if not text:
            return None
    for label in language_labels:
        if not label:
            return None

    language_profiles = {}
    for i in range(len(language_labels)):
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
    for dictionary in language_profiles.values():
        for key in dictionary.keys():
            features.append(key)
    return sorted(features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) or not isinstance(original_text, list):
        return None

    text_vector = []
    for word in get_language_features(language_profiles):
        if word in original_text:
            for dictionary in language_profiles:
                if word in language_profiles[dictionary]:
                    text_vector.append(language_profiles[dictionary][word])
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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, (int, float)):
            return None
    for number in known_text_vector:
        if not isinstance(number, (int, float)):
            return None

    distance_sum = 0
    for i in range(len(unknown_text_vector)):
        distance_sum += (unknown_text_vector[i] - known_text_vector[i]) ** 2
    return round(distance_sum ** 0.5, 5)


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

    label_vector = {}
    for i in range(len(known_text_vectors)):
        label_vector[language_labels[i]] = calculate_distance(unknown_text_vector,
                                                              known_text_vectors[i])
    for key, value in label_vector.items():
        if value == min(label_vector.values()):
            possible_language = [key, value]
    return possible_language


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
    for number in unknown_text_vector:
        if not isinstance(number, (int, float)):
            return None
    for number in known_text_vector:
        if not isinstance(number, (int, float)):
            return None

    distance = 0
    for i in range(len(unknown_text_vector)):
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
            or not isinstance(language_labels, list) \
            or not isinstance(k, int) \
            or not isinstance(metric, str):
        return None
    if len(known_text_vectors) != len(language_labels):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, (int, float)):
            return None

    distances = []
    if metric == 'manhattan':
        for vector in known_text_vectors:
            distances.append(calculate_distance_manhattan(unknown_text_vector, vector))
    else:
        for vector in known_text_vectors:
            distances.append(calculate_distance(unknown_text_vector, vector))

    k_nearest = sorted(zip(language_labels, distances), key=lambda x: x[1])[:k]
    language_freq = {}
    for language in k_nearest:
        if language[0] not in language_freq:
            language_freq[language[0]] = 1
        else:
            language_freq[language[0]] += 1
    possible_language = [max(language_freq, key=language_freq.get), k_nearest[0][1]]
    return possible_language


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
