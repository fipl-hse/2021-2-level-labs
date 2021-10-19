"""
Lab 2
Language classification
"""
from math import fabs

from lab_1.main import tokenize, remove_stop_words


# 4
def elements_isinstance(list_with_elem: list, type_of_elem: type) -> True or False:
    """
    Checks types of elements with isinstance()
    :param list_with_elem: a list with some elements
    :param type_of_elem: type of element we need
    :return: True
    """
    for element in list_with_elem:
        if not isinstance(element, type_of_elem):
            return False
    return True


def vectorization(language_profiles: dict, list_of_features: list, word: tuple) -> list:
    """
    Replace elements in list_of features with their
        frequency from language_profiles
    :param list_of_features: list of unique words
    :param language_profiles: a dictionary of dictionaries - language profiles
    :param word: a tuple with (index,word) from enumerate(list_of_features)
    """
    test_element = 0
    for profile in language_profiles:
        for element in language_profiles[profile]:
            if word[1] == element and language_profiles[profile][element] > test_element:
                list_of_features[word[0]] = language_profiles[profile][element]
                test_element = language_profiles[profile][element]
    return list_of_features


def vectorization_sparse(language_profiles: dict, list_of_features: list, word: tuple) -> list:
    """
    Replace elements in list_of features with their
        position in text and frequency from language_profiles
    :param list_of_features: list of unique words
    :param language_profiles: a dictionary of dictionaries - language profiles
    :param word: a tuple with (index,word) from enumerate(list_of_features)
    """
    test_element_sparse = 0
    for profile in language_profiles:
        for element in language_profiles[profile]:
            if word[1] == element and language_profiles[profile][element] > test_element_sparse:
                list_of_features[word[0]] = [word[0], language_profiles[profile][element]]
                test_element_sparse = language_profiles[profile][element]
    return list_of_features


def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list) or not elements_isinstance(tokens, str):
        return None
    freq_dict = {}
    for token1 in tokens:
        if token1 in freq_dict:
            freq_dict[token1] += 1
        else:
            freq_dict[token1] = 1
    for key in freq_dict.keys():
        freq_dict[key] = round(freq_dict[key] / len(tokens), 5)
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
            or not elements_isinstance(texts_corpus, list) \
            or not elements_isinstance(language_labels, str):
        return None
    for tokens in enumerate(texts_corpus):
        texts_corpus[tokens[0]] = get_freq_dict(tokens[1])
    circle = 0
    language_profiles = {}
    for element in texts_corpus:
        language_profiles[language_labels[circle]] = element
        circle += 1
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
    for element in language_profiles:
        for i in language_profiles[element]:
            features.append(i)
    features.sort()
    return features


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) \
            or not isinstance(language_profiles, dict) \
            or not elements_isinstance(original_text, str):
        return None
    list_of_features = get_language_features(language_profiles)
    for word in enumerate(list_of_features):
        if word[1] in original_text:
            vectorization(language_profiles, list_of_features, word)
        else:
            list_of_features[word[0]] = 0
    return list_of_features


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list) \
            or not elements_isinstance(unknown_text_vector, (int, float)) \
            or not elements_isinstance(known_text_vector, (int, float)):
        return None
    distance = 0
    for element in enumerate(unknown_text_vector):
        distance += pow(element[1] - known_text_vector[element[0]], 2)
    return round(pow(distance, 0.5), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    items = [unknown_text_vector, known_text_vectors, language_labels]
    types = [(int, float), list, str]
    for element in enumerate(items):
        if not isinstance(element[1], list):
            return None
        if not elements_isinstance(element[1], types[element[0]]):
            return None
    if len(known_text_vectors) != len(language_labels):
        return None
    distance = 1
    label = ''
    for known_text_vector in enumerate(known_text_vectors):
        if calculate_distance(unknown_text_vector, known_text_vector[1]) < distance:
            distance = calculate_distance(unknown_text_vector, known_text_vector[1])
            label = language_labels[known_text_vector[0]]
    label_distance = [label, distance]
    return label_distance


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vector, list) \
            or not elements_isinstance(unknown_text_vector, (int, float)) \
            or not elements_isinstance(known_text_vector, (int, float)):
        return None
    distance = 0
    for element in enumerate(unknown_text_vector):
        distance += fabs(element[1] - known_text_vector[element[0]])
    return round(distance, 5)


def min_distance_to_neighbour(elements: list, label: str) -> float:
    """
    Calculates minimum distance in one label
    :param elements: a dictionary
    :param label: a label
    """
    min_distance = 10
    for i in elements:
        if label == i['label']:
            if i['distance'] < min_distance:
                min_distance = i['distance']
    return min_distance


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
    items = [unknown_text_vector, known_text_vectors, language_labels]
    types_knn = [(int, float), list, str]
    for element in enumerate(items):
        if not isinstance(element[1], list):
            return None
        if not elements_isinstance(element[1], types_knn[element[0]]):
            return None
    if not isinstance(k, int):
        return None
    if len(known_text_vectors) != len(language_labels):
        return None
    distance_of_vectors = []
    elements = []
    if metric == 'manhattan':
        for vector in known_text_vectors:
            distance_of_vectors.append(calculate_distance_manhattan(unknown_text_vector, vector))
    elif metric == 'euclid':
        for vector in known_text_vectors:
            distance_of_vectors.append(calculate_distance(unknown_text_vector, vector))
    else:
        return None
    for distance_of_vector in enumerate(distance_of_vectors):
        elements.append({'distance': distance_of_vector[1],
                         'label': language_labels[distance_of_vector[0]]})
    elements = sorted(elements, key=lambda x: x['distance'])
    elements = elements[:k]
    labels_count = {}
    for i in elements:
        if i['label'] in labels_count:
            labels_count[i['label']] += 1
        else:
            labels_count[i['label']] = 1
    min_labels_dist = 0
    super_label = ''
    for key in labels_count.keys():
        if labels_count[key] > min_labels_dist:
            min_labels_dist = labels_count[key]
            super_label = key
        if labels_count[key] == min_labels_dist:
            if min_distance_to_neighbour(elements, key) \
                    < min_distance_to_neighbour(elements, super_label):
                super_label = key
    return [super_label, elements[0]['distance']]


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) \
            or not (original_text, list) \
            or not elements_isinstance(original_text, str) \
            or not language_profiles:
        return None
    list_of_features = get_language_features(language_profiles)
    for word in enumerate(list_of_features):
        if word[1] in original_text:
            vectorization_sparse(language_profiles, list_of_features, word)
        else:
            list_of_features[word[0]] = 0
    while 0 in list_of_features:
        for element in list_of_features:
            if element == 0:
                list_of_features.remove(element)
    return list_of_features


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vector, list) \
            or not elements_isinstance(unknown_text_vector, list) \
            or not elements_isinstance(known_text_vector, list):
        return None
    distance = 0
    unknown_text_vector_dict = dict(unknown_text_vector)
    for element in known_text_vector:
        if element[0] in unknown_text_vector_dict.keys():
            unknown_text_vector_dict[element[0]] -= element[1]
        else:
            unknown_text_vector_dict[element[0]] = element[1]
    for element in unknown_text_vector_dict.values():
        distance += pow(element, 2)
    return round(pow(distance, 0.5), 5)


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
    items_sparse = [unknown_text_vector, known_text_vectors, language_labels]
    types_knn = [list, list, str]
    for element in enumerate(items_sparse):
        if not isinstance(element[1], list):
            return None
        if not elements_isinstance(element[1], types_knn[element[0]]):
            return None
    if len(known_text_vectors) != len(language_labels):
        return None
    distance_of_vectors = []
    elements = []
    for vector in known_text_vectors:
        distance_of_vectors.append(calculate_distance_sparse(unknown_text_vector, vector))
    for distance_of_vector in enumerate(distance_of_vectors):
        elements.append({'distance': distance_of_vector[1],
                         'label': language_labels[distance_of_vector[0]]})
    elements = sorted(elements, key=lambda x: x['distance'])
    elements = elements[:k]
    labels_count = {}
    for i in elements:
        if i['label'] in labels_count:
            labels_count[i['label']] += 1
        else:
            labels_count[i['label']] = 1
    min_labels_dist = 0
    super_label = ''
    for key in labels_count.keys():
        if labels_count[key] > min_labels_dist:
            min_labels_dist = labels_count[key]
            super_label = key
        if labels_count[key] == min_labels_dist:
            if min_distance_to_neighbour(elements, key) \
                    < min_distance_to_neighbour(elements, super_label):
                super_label = key
    return [super_label, elements[0]['distance']]
