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
    freq_dict = {}
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    length = len(tokens)
    for key, value in freq_dict.items():
        value = round(value / length, 5)
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
    if (not isinstance(texts_corpus, list)) or (not isinstance(language_labels, list)):
        return None
    language_profiles = {}
    dictionary_lst = []
    for text in texts_corpus:
        if not isinstance(text, list):
            return None
        dictionary_lst.append(get_freq_dict(text))
    for index, label in enumerate(language_labels):
        language_profiles[label] = dictionary_lst[index]
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
    for values in language_profiles.values():
        for key in values.keys():
            if key not in unique_words:
                unique_words.append(key)
    if len(unique_words) == 0:
        return None
    for word in unique_words:
        if not isinstance(word, str):
            return None
    return sorted(unique_words)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if (not isinstance(original_text, list)) or (not isinstance(language_profiles, dict)):
        return None
    unique_words = get_language_features(language_profiles)
    text_vector = []
    for word in unique_words:
        if word not in original_text:
            text_vector.append(0)
        else:
            for profile in language_profiles.values():
                for k in profile.keys():
                    if k == word:
                        value = profile.get(word)
                        text_vector.append(value)
    return text_vector


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if (not isinstance(unknown_text_vector, list)) or (not isinstance(known_text_vector, list)):
        return None
    dist = 0
    for index_un, freq_un in enumerate(unknown_text_vector):
        for number in unknown_text_vector:
            if not isinstance(number, (int, float)):
                return None
        for number in known_text_vector:
            if not isinstance(number, (int, float)):
                return None
        for index_kn, freq_kn in enumerate(known_text_vector):
            if index_un == index_kn:
                dist += (freq_un - freq_kn) ** 2
    return round(sqrt(dist), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if (not isinstance(unknown_text_vector, list)) or (not isinstance(known_text_vectors, list)) \
            or (not isinstance(language_labels, list)):
        return None
    distance_lst = []
    for distance in known_text_vectors:
        dist = calculate_distance(unknown_text_vector, distance)
        distance_lst.append(dist)
    predict = []
    min_dist = distance_lst.index(min(distance_lst))
    min_label = language_labels[min_dist]
    predict.append(min_label)
    predict.append(min(distance_lst))
    if len(known_text_vectors) != len(language_labels):
        return None
    for element in predict:
        if not isinstance(element, (str, float)):
            return None
    return predict


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if (not isinstance(unknown_text_vector, list)) or (not isinstance(known_text_vector, list)):
        return None
    dist = 0
    for index_un, freq_un in enumerate(unknown_text_vector):
        for number in unknown_text_vector:
            if not isinstance(number, (int, float)):
                return None
        for number in known_text_vector:
            if not isinstance(number, (int, float)):
                return None
        for index_kn, freq_kn in enumerate(known_text_vector):
            if index_un == index_kn:
                dist += abs(freq_un - freq_kn)
    return dist


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
    if (not isinstance(unknown_text_vector, list)) or (not isinstance(known_text_vectors, list)) \
            or (not isinstance(language_labels, list)) or (not isinstance(k, int)) \
            or not isinstance(metric, str):
        return None
    distances = []
    for vector in known_text_vectors:
        if metric == 'manhattan':
            dist = calculate_distance_manhattan(unknown_text_vector, vector)
            distances.append(dist)
        elif metric == 'euclid':
            dist = calculate_distance(unknown_text_vector, vector)
            distances.append(dist)
    k_distances = sorted(distances)
    k_distances = k_distances[:(k + 1)]
    labels = []
    for dist in k_distances:
        ind = distances.index(dist)
        if len(language_labels) == len(known_text_vectors):
            label = language_labels[ind]
            labels.append(label)
        else:
            return None
    labels_dict = {}
    for label in labels:
        if isinstance(label, str):
            if label in labels_dict:
                labels_dict[label] += 1
            else:
                labels_dict[label] = 1
        else:
            return None
    predict_label = max(labels_dict, key=labels_dict.get)
    predict_result = [predict_label, round(min(distances), 5)]
    return predict_result


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if (not isinstance(original_text, list)) or (not isinstance(language_profiles, dict)):
        return None
    unique_words = get_language_features(language_profiles)
    text_vector = []
    for word in unique_words:
        if word in original_text:
            for profile in language_profiles.values():
                for k in profile.keys():
                    if k == word:
                        value = profile.get(word)
                        text_vector.append([unique_words.index(word), value])
    return text_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if (not isinstance(unknown_text_vector, list)) or (not isinstance(known_text_vector, list)):
        return None
    dist = 0
    vector = []
    for lst_un in unknown_text_vector:
        for element in unknown_text_vector:
            if not isinstance(element, list):
                return None
        for element in known_text_vector:
            if not isinstance(element, list):
                return None
        vector.append(lst_un[0])
        for lst_kn in known_text_vector:
            vector.append(lst_kn[0])
    unknown_vector = [0] * max(vector)
    known_vector = [0] * max(vector)
    for number in unknown_text_vector:
        unknown_vector.insert(number[0], number[1])
    for number in known_text_vector:
        known_vector.insert(number[0], number[1])
    for index_un, freq_un in enumerate(unknown_vector):
        for index_kn, freq_kn in enumerate(known_vector):
            if index_un == index_kn:
                dist += (freq_un - freq_kn) ** 2
    return round(sqrt(dist), 5)


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
    if (not isinstance(unknown_text_vector, list)) or (not isinstance(known_text_vectors, list)) \
            or (not isinstance(language_labels, list)) or (not isinstance(k, int)):
        return None
    distances = []
    for vector in known_text_vectors:
        dst = calculate_distance_sparse(unknown_text_vector, vector)
        distances.append(dst)
    k_distances = sorted(distances)
    k_distances = k_distances[:(k + 1)]
    labels = []
    for dist in k_distances:
        ind = distances.index(dist)
        if len(language_labels) == len(known_text_vectors):
            label = language_labels[ind]
            labels.append(label)
        else:
            return None
    labels_dict = {}
    for label in labels:
        if isinstance(label, str):
            if label in labels_dict:
                labels_dict[label] += 1
            else:
                labels_dict[label] = 1
        else:
            return None
    predict_label = max(labels_dict, key=labels_dict.get)
    predict_result = [predict_label, round(min(distances), 5)]
    return predict_result
