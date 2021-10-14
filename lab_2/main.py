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
    for i in tokens:
        if not isinstance(i, str):
            return None
    freq_dict = {}
    for i in tokens:
        if i not in freq_dict:
            freq_dict[i] = 1
        else:
            freq_dict[i] += 1
    for i in freq_dict:
        freq_dict[i] = round(freq_dict[i] / len(tokens), 5)
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
    for corpus in texts_corpus:
        if not isinstance(corpus, list):
            return None
        for token in corpus:
            if not isinstance(token, str):
                return None
    for label in language_labels:
        if not isinstance(label, str):
            return None
    language_profiles = {key: get_freq_dict(value) for key, value
                         in zip(language_labels, texts_corpus)}
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
    text_vector = []
    for word in get_language_features(language_profiles):
        if word in original_text:
            for freq_dict in language_profiles.values():
                for key in freq_dict:
                    if key == word:
                        text_vector.append(freq_dict[key])
                        break
        else:
            text_vector.append(0)
    if not text_vector:
        return None
    return text_vector

# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list)\
            or not isinstance(known_text_vector, list):
        return None
    for i in unknown_text_vector:
        if not isinstance(i, int) and not isinstance(i, float):
            return None
    for i in known_text_vector:
        if not isinstance(i, int) and not isinstance(i, float):
            return None
    distance = 0
    for a, b in zip(unknown_text_vector, known_text_vector):
        distance += (a-b)**2
    return round(distance**0.5, 5)



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
            or not isinstance(language_labels, list)
            or len(known_text_vectors) != len(language_labels)):
        return None
    for i in unknown_text_vector:
        if not isinstance(i, (float, int)):
            return None
    for i in known_text_vectors:
        if not isinstance(i, list):
            return None
    for i in language_labels:
        if not isinstance(i, str):
            return None
    dictionary = {}
    for i in range(len(known_text_vectors)):
        dictionary[language_labels[i]] = calculate_distance(unknown_text_vector, known_text_vectors[i])
    min_value = min(dictionary.values())
    for key, value in dictionary.items():
        if value == min_value:
            return [key, value]

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
