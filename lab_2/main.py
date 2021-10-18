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
    freq_dict = {}
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token not in freq_dict:
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1
    for key, value in freq_dict.items():
        value = round(value / len(tokens), 5)
        freq_dict[key] = value
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
    language_profiles = {}
    for text in texts_corpus:
        if not isinstance(text, list):
            return None
        freq_dict = get_freq_dict(text)
        language_profiles[language_labels[texts_corpus.index(text)]] = freq_dict
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    unique_words = []
    for tokens in language_profiles.values():
        unique_words.extend(tokens)
    if not unique_words:
        return None
    unique_words.sort()
    return unique_words


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or not isinstance(language_profiles, dict):
        return None
    text_vector = []
    words_freq = list(language_profiles.values())
    words_freq_dict = {}
    for dicts in words_freq:
        for key, value in dicts.items():
            if key in words_freq_dict:
                if words_freq_dict.get(key) > dicts[key]:
                    continue
            words_freq_dict[key] = value
    for unique_word in get_language_features(language_profiles):
        if unique_word in original_text:
            text_vector.append(words_freq_dict.get(unique_word))
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
    distance = 0
    counter = 0
    for vector_value in unknown_text_vector:
        if not isinstance(vector_value, (int, float)) or not \
                isinstance(known_text_vector[counter], (int, float)):
            return None
        distance += (vector_value - known_text_vector[counter]) ** 2
        counter += 1
    return round(distance**0.5, 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list) or not \
        isinstance(known_text_vectors, list) or not \
            isinstance(language_labels, list) or not \
            len(known_text_vectors) == len(language_labels):
        return None
    vectors_distances = []
    min_distance = []
    for known_text_vector in known_text_vectors:
        if not isinstance(known_text_vector, list):
            return None
        vectors_distances.append(calculate_distance(unknown_text_vector, known_text_vector))
    min_distance_vector = min(vectors_distances)
    min_distance.extend([language_labels[vectors_distances.index(min_distance_vector)], min_distance_vector])
    return min_distance



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
    distance = 0
    counter = 0
    for vector_value in unknown_text_vector:
        if not isinstance(vector_value, (int, float)) or not \
                isinstance(known_text_vector[counter], (int, float)):
            return None
        distance += abs(vector_value - known_text_vector[counter])
        counter += 1
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
