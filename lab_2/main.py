"""
Lab 2
Language classification
"""
from math import fabs
from lab_1.main import tokenize, remove_stop_words


def isinstance_for_elem(list_elem: list, type_of_elem: type) -> True or False:
    """
    Checks types of elements with isinstance()
    :param list_elem: list
    :param type_of_elem: type of elem
    :return: True
    """
    for elem in list_elem:
        if not isinstance(elem, type_of_elem):
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
    null = 0
    for profile in language_profiles:
        for element in language_profiles[profile]:
            if word[1] == element and language_profiles[profile][element] > null:
                list_of_features[word[0]] = language_profiles[profile][element]
                null = language_profiles[profile][element]
    return list_of_features


# 4
def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list) or not isinstance_for_elem(tokens, str):
        return None
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    for key in freq_dict:
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
            or not isinstance_for_elem(texts_corpus, list) \
            or not isinstance_for_elem(language_labels, str):
        return None
    language_profiles = {}
    for corpus in enumerate(texts_corpus):
        texts_corpus[corpus[0]] = get_freq_dict(corpus[1])
    for corpus in enumerate(texts_corpus):
        language_profiles[language_labels[corpus[0]]] = corpus[1]
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
    for language_profile in language_profiles:
        for i in language_profiles[language_profile]:
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
            or not isinstance_for_elem(original_text, str):
        return None
    features = get_language_features(language_profiles)
    for word in enumerate(features):
        if word[1] in original_text:
            vectorization(language_profiles, features, word)
        else:
            features[word[0]] = 0
    return features


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list) \
            or not isinstance_for_elem(unknown_text_vector, (int, float)) \
            or not isinstance_for_elem(known_text_vector, (int, float)):
        return None
    distance = 0
    for i in enumerate(unknown_text_vector):
        distance += pow(i[1] - known_text_vector[i[0]], 2)
    return round(pow(distance, 0.5), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not (isinstance(unknown_text_vector, list)
            and isinstance(known_text_vectors, list)
            and isinstance(language_labels, list)
            and isinstance_for_elem(unknown_text_vector, (int, float))
            and isinstance_for_elem(known_text_vectors, list)
            and isinstance_for_elem(language_labels, str)
            and len(known_text_vectors) == len(language_labels)):
        return None
    distance = 1
    label = ''
    for known_text_vector in enumerate(known_text_vectors):
        if calculate_distance(unknown_text_vector, known_text_vector[1]) < distance:
            distance = calculate_distance(unknown_text_vector, known_text_vector[1])
            label = language_labels[known_text_vector[0]]
    label_and_distance = [label, distance]
    return label_and_distance


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
            or not isinstance_for_elem(unknown_text_vector, (int, float)) \
            or not isinstance_for_elem(known_text_vector, (int, float)):
        return None
    distance = 0
    for i in enumerate(unknown_text_vector):
        distance += fabs(i[1] - known_text_vector[i[0]])
    return round(distance, 5)


def min_distance_in_label(elements: list, label: str) -> float:
    """
    Calculates minimum distance in one label
    :param elements: a dictionary
    :param label: a label
    """
    min_distance = 100
    for i in elements:
        if label == i['label']:
            if i['distance'] < min_distance:
                min_distance = i['distance']
    return min_distance


def freq_dict_for_labels(labels) -> dict:
    """
    Calculates frequencies of given labels
    :param labels: a list of labels
    :return: a dictionary with frequencies
    """
    count_labels = {}
    for label in labels:
        if label['label'] in count_labels:
            count_labels[label['label']] += 1
        else:
            count_labels[label['label']] = 1
    return count_labels


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
            and isinstance(known_text_vectors, list)
            and isinstance(language_labels, list)
            and isinstance(k, int)
            and isinstance_for_elem(unknown_text_vector, (int, float))
            and isinstance_for_elem(known_text_vectors, list)
            and len(known_text_vectors) == len(language_labels)
            and isinstance_for_elem(language_labels, str)):
        return None
    distance_of_vectors = []
    if metric == 'manhattan':
        for known_vector in known_text_vectors:
            distance_of_vectors.append(calculate_distance_manhattan(unknown_text_vector,
                                                                    known_vector))
    elif metric == 'euclid':
        for known_vector in known_text_vectors:
            distance_of_vectors.append(calculate_distance(unknown_text_vector, known_vector))
    else:
        return None
    elements = []
    for distance_of_vector in enumerate(distance_of_vectors):
        elements.append({'distance': distance_of_vector[1],
                         'label': language_labels[distance_of_vector[0]]})
    elements = sorted(elements, key=lambda x: x['distance'])
    elements = elements[:k]
    count_labels = freq_dict_for_labels(elements)
    min_labels_dist = 0
    result_label = ''
    for key, value in count_labels.items():
        if value > min_labels_dist:
            min_labels_dist = value
            result_label = key
        if value == min_labels_dist:
            if min_distance_in_label(elements, key) < min_distance_in_label(elements, result_label):
                result_label = key
    returning = [result_label, elements[0]['distance']]
    return returning


# 10

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
