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
    if not isinstance(tokens, list) or None in tokens:
        return None
    freq_dict = {}
    for word in tokens:
        freq_dict[word] = round(tokens.count(word)/len(tokens), 5)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not isinstance(texts_corpus, list) \
            or not isinstance(language_labels, list) \
            or None in texts_corpus \
            or None in language_labels:
        return None
    language_profiles = {}
    for tokens in texts_corpus:
        if None in tokens \
                or not isinstance(tokens, list):
            return None
        freq_dict = get_freq_dict(tokens)
        language_profiles[language_labels[texts_corpus.index(tokens)]] = freq_dict
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict)\
            or language_profiles == {}:
        return None
    uniq_list = []
    for freq_dict in language_profiles.values():
        uniq_list.extend(list(freq_dict.keys()))
    uniq_list = list(set(uniq_list))
    uniq_list = sorted(uniq_list)
    return uniq_list


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list)\
            or not isinstance(language_profiles, dict):
        return None
    text_features = get_language_features(language_profiles)
    text_vector = []
    for word in text_features:
        if word in original_text:
            for dic in language_profiles.values():
                if word in dic:
                    text_vector.append(dic[word])
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
    if not isinstance(unknown_text_vector, list)\
            or not isinstance(known_text_vector, list):
        return None
    for num in unknown_text_vector:
        if not isinstance(num, (int, float)):
            return None
    for num in known_text_vector:
        if not isinstance(num, (int, float)):
            return None
    distance = 0
    for index, kor in enumerate(unknown_text_vector):
        distance += (kor - known_text_vector[index])**2
    distance = round(distance**0.5, 5)
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
            or not isinstance(language_labels, list)\
            or len(language_labels) != len(known_text_vectors):
        return None
    predictions = []
    for vector in known_text_vectors:
        if not isinstance(vector, list):
            return None
        distance = calculate_distance(unknown_text_vector, vector)
        index = known_text_vectors.index(vector)
        lang_pred = [language_labels[index], distance]
        predictions.append(lang_pred)
    min_dist = ['unk', 100]
    for item in predictions:
        if item[1] < min_dist[1]:
            min_dist = item
    return min_dist
# 8


def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vector, list):
        return None
    for num in unknown_text_vector:
        if not isinstance(num, (float, int)):
            return None
    for num in known_text_vector:
        if not isinstance(num, (float, int)):
            return None
    distance = 0
    for index, kor in enumerate(unknown_text_vector):
        distance += abs(kor - known_text_vector[index])
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
