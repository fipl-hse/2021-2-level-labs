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
    if not isinstance(tokens, list) or not all(isinstance(i, str) for i in tokens):
        return None
    freq_dict = {}
    for element in tokens:
        if element not in freq_dict:
            freq_dict[element] = 1
        freq_dict[element] +=1
    for element in freq_dict:
        freq_dict[element] = round(tokens.count(element) / len(tokens), 5)
    return freq_dict



def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not isinstance (texts_corpus, list) or not isinstance (language_labels, list) \
            or not all(isinstance(i, list) for i in texts_corpus) \
            or not all(isinstance(a, str) for a in language_labels):
        return None
    freq_dictionary = [get_freq_dict(element) for element in texts_corpus]
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
    unique_words = []
    for language in language_profiles.values():
        for key in language.keys():
            unique_words.append(key)
    if not unique_words:
        return None
    return sorted(unique_words)


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
    for element in get_language_features(language_profiles):
        if element in original_text:
            for freq_dict in language_profiles.values():
                if element in freq_dict:
                    text_vector.append(freq_dict[element])
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
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vector, list) \
            or not all(isinstance(i, (int, float)) for i in unknown_text_vector) \
            or not all(isinstance(i, (int, float)) for i in known_text_vector):
        return None

    distance1 = 0
    for unknown_vector, known_vector in zip(unknown_text_vector, known_text_vector):
        distance1 += (unknown_vector - known_vector) ** 2
        distance = round(distance1 ** 0.5, 5)
    return distance


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
            or not all(isinstance(i,(int, float)) for i in unknown_text_vector) \
            or not all(isinstance(v, list) for v in known_text_vectors) \
            or not all(isinstance(l, str) for l in language_labels) \
            or len(known_text_vectors) != len(language_labels):
        return None
    language_score = ['', 1]
    for language, text_vector in enumerate(known_text_vectors):
        distance = calculate_distance(unknown_text_vector, text_vector)
        if language_score[1] > distance:
            language_score = [language_labels[language], distance]
    return language_score


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
