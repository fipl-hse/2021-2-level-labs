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
    if not (isinstance(tokens, list)
            and all(isinstance(i, str) for i in tokens)):
        return None
    freq_dict = {}
    for i in tokens:
        freq_dict[i] = round(tokens.count(i) / len(tokens), 5)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(texts_corpus, list)
            and all(isinstance(i, list) for i in texts_corpus)
            and isinstance(language_labels, list)
            and all(isinstance(i, str) for i in language_labels)):
        return None
    language_profiles = {}
    for index, label in enumerate(language_labels):
        language_profiles[label] = get_freq_dict(texts_corpus[index])
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(language_profiles, dict) and language_profiles != {}
            and all(isinstance(i, str) for i in language_profiles)
            and all(isinstance(i, dict) for i in language_profiles.values())):
        return None
    features = [i for n in language_profiles.values() for i in n if all(n)]
    features.sort()
    return features


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(original_text, list) and language_profiles != {}
            and all(isinstance(i, str) for i in original_text)
            and isinstance(language_profiles, dict)
            and all(isinstance(i, dict) for i in language_profiles.values())):
        return None
    features = get_language_features(language_profiles)
    vector_freq_dict = dict.fromkeys(features, 0)
    for word in features:
        if word not in original_text:
            continue
        for freq_dict in language_profiles.values():
            for key, value in freq_dict.items():
                if key != word or value <= vector_freq_dict[key]:
                    continue
                vector_freq_dict[key] = value
    text_vector = list(vector_freq_dict.values())
    return text_vector


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(i, (float, int)) for i in unknown_text_vector)
            and isinstance(known_text_vector, list)
            and all(isinstance(i, (float, int)) for i in known_text_vector)):
        return None
    distance = 0
    for unknown_vector, known_vector in zip(unknown_text_vector, known_text_vector):
        distance += (unknown_vector - known_vector) ** 2
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
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(i, (float, int)) for i in unknown_text_vector)
            and isinstance(known_text_vectors, list)
            and all(isinstance(i, list) for i in known_text_vectors)
            and isinstance(language_labels, list)
            and all(isinstance(i, str) for i in language_labels)
            and len(known_text_vectors) == len(language_labels)):
        return None
    list_of_scores = [[] for i in range(len(known_text_vectors))]
    k = 0
    while True:
        if k == len(known_text_vectors):
            break
        list_of_scores[k].append(calculate_distance(unknown_text_vector, known_text_vectors[k]))
        list_of_scores[k].append(language_labels[k])
        k += 1
    list_of_scores.sort()
    list_of_scores[0][0], list_of_scores[0][1] = list_of_scores[0][1], list_of_scores[0][0]
    print(list_of_scores[0])
    return list_of_scores[0]


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(i, (float, int)) for i in unknown_text_vector)
            and isinstance(known_text_vector, list)
            and all(isinstance(i, (float, int)) for i in known_text_vector)):
        return None
    distance = 0
    for unknown_vector, known_vector in zip(unknown_text_vector, known_text_vector):
        distance += abs(unknown_vector - known_vector)
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
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(i, (int, float)) for i in unknown_text_vector)
            and isinstance(known_text_vectors, list)
            and all(isinstance(i, list) for i in known_text_vectors)
            and isinstance(language_labels, list)
            and all(isinstance(i, str) for i in language_labels)
            and len(known_text_vectors) == len(language_labels)):
        return None
    list_of_scores = [[] for i in range(len(known_text_vectors))]
    list_knn = []
    list_newest = []
    dict_counter = {}
    counter = 0
    distance = 0
    while True:
        if counter == len(known_text_vectors):
            break
        if metric == 'euclid':
            distance = calculate_distance(unknown_text_vector, known_text_vectors[counter])
        if metric == 'manhattan':
            distance = calculate_distance_manhattan(unknown_text_vector,
                                                    known_text_vectors[counter])
        list_of_scores[counter].append(distance)
        list_of_scores[counter].append(language_labels[counter])
        counter += 1
    list_of_scores.sort()
    while k != -1:
        list_of_scores[k][0], list_of_scores[k][1] = list_of_scores[k][1], list_of_scores[k][0]
        k -= 1
    for i in list_of_scores[:k]:
        list_knn.append(i[0])
    for i in list_knn:
        dict_counter[i] = list_knn.count(i)
    right_label = sorted(dict_counter, key=dict_counter.get, reverse=True)[0]
    list_newest.extend([right_label, list_of_scores[0][1]])
    return list_newest


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(original_text, list) and language_profiles != {}
            and all(isinstance(i, str) for i in original_text)
            and isinstance(language_profiles, dict)
            and all(isinstance(i, dict) for i in language_profiles.values())):
        return None
    features = get_language_features(language_profiles)
    vector_freq_dict = dict.fromkeys(features, 0)
    new_list = []
    for word in features:
        if word not in original_text:
            continue
        for freq_dict in language_profiles.values():
            for key, value in freq_dict.items():
                if key != word:
                    continue
                if value <= vector_freq_dict[key]:
                    continue
                vector_freq_dict[key] = value
    list_of_scores = list(vector_freq_dict.values())
    k = 0
    for i in list_of_scores:
        if k == len(list_of_scores):
            break
        if i == 0:
            k += 1
            continue
        new_list.append([k, i])
        k += 1
    return new_list


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(i, list) for i in unknown_text_vector)
            and isinstance(known_text_vector, list)
            and all(isinstance(i, list) for i in known_text_vector)):
        return None

    unknown_text_vector = dict(unknown_text_vector)
    known_text_vector = dict(known_text_vector)
    mixed_dict_vector = unknown_text_vector | known_text_vector
    for key, value in unknown_text_vector.items():
        if key in known_text_vector:
            mixed_dict_vector[key] = value - known_text_vector[key]
    distance = 0
    for value in mixed_dict_vector.values():
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
    if not (isinstance(unknown_text_vector, list)
            and all(isinstance(i, list) for i in unknown_text_vector)
            and isinstance(known_text_vectors, list)
            and all(isinstance(i, list) for i in known_text_vectors)
            and isinstance(language_labels, list)
            and all(isinstance(i, str) for i in language_labels)
            and len(known_text_vectors) == len(language_labels)):
        return None
    list_of_scores = [[] for i in range(len(known_text_vectors))]
    list_knn = []
    list_newest = []
    dict_counter = {}
    counter = 0
    while True:
        if counter == len(known_text_vectors):
            break
        distance = calculate_distance_sparse(unknown_text_vector,
                                             known_text_vectors[counter])
        list_of_scores[counter].append(distance)
        list_of_scores[counter].append(language_labels[counter])
        counter += 1
    list_of_scores.sort()
    while k != -1:
        list_of_scores[k][0], list_of_scores[k][1] = list_of_scores[k][1], list_of_scores[k][0]
        k -= 1
    for i in list_of_scores[:k]:
        list_knn.append(i[0])
    for i in list_knn:
        dict_counter[i] = list_knn.count(i)
    right_label = sorted(dict_counter, key=dict_counter.get, reverse=True)[0]
    list_newest.extend([right_label, list_of_scores[0][1]])
    return list_newest
