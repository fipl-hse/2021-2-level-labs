"""
Lab 2
Language classification
"""

from math import fabs
from lab_1.main import tokenize, remove_stop_words

# 4
def type_elements(elements_list: list, type_of_elements: type) -> True or False:
    """
    Checks list elements
    :param elements_list: a list with elements
    :param type_of_elements: type
    :return: True or False
    """
    for element in elements_list:
        if not isinstance(element, type_of_elements):
            return False
    return True


def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list) or not type_elements(tokens, str):
        return None
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    for element in freq_dict:
        freq_dict[element] = round(freq_dict[element] / len(tokens), 5)
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
        or not type_elements(texts_corpus, list) \
        or not type_elements(language_labels, str):
        return None
    for text in enumerate(texts_corpus):
        texts_corpus[text[0]] = get_freq_dict(text[1])
    language_profiles = {}
    for elements in enumerate(texts_corpus):
        language_profiles[language_labels[elements[0]]] = elements[1]
    return language_profiles





def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    if not language_profiles:
        return None
    uniq_words = []
    for profile in language_profiles:
        for element in language_profiles[profile]:
            uniq_words.append(element)
    uniq_words.sort()
    return uniq_words

def exchange_words(element: tuple, uniq_words: list, language_profiles: dict) -> list:
    """
    Replace elements in uniq_words with their
        frequency from language_profiles
    :param uniq_words: list of unique words
    :param language_profiles: a dictionary of dictionaries - language profiles
    :param element: a tuple with (index,word) from enumerate(uniq_words)
    """
    freq = 0
    for profile in language_profiles:
        for prof_dict in language_profiles[profile]:
            if element[1]  == prof_dict and language_profiles[profile][prof_dict] > freq:
                uniq_words[element[0]] = language_profiles[profile][prof_dict]
                freq = language_profiles[profile][prof_dict]
    return uniq_words


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) \
            or not(language_profiles, dict) \
            or not type_elements(original_text, str):
        return None
    uniq_words = get_language_features(language_profiles)
    for element in enumerate(uniq_words):
        if element[1] in original_text:
            exchange_words(element, uniq_words, language_profiles)
        else:
            uniq_words[element[0]] = 0
    return uniq_words




# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) \
        or not isinstance (known_text_vector, list) \
        or not type_elements(unknown_text_vector, (int, float)) \
        or not type_elements(known_text_vector, (int, float)):
        return None
    distance = 0
    for element in enumerate(unknown_text_vector):
        dif = element[1] - known_text_vector[element[0]]
        distance += pow(dif, 2)
    distance = pow(distance, 0.5)
    return round(distance, 5)



def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    texts = [unknown_text_vector, known_text_vectors, language_labels]
    types = [(int, float),list , str]
    for element in enumerate(texts):
        if not isinstance(element[1], list):
            return None
        if not type_elements(element[1], types[element[0]]):
            return None
    if len(known_text_vectors) != len(language_labels):
        return None
    distance = 10
    label = ''
    for element in enumerate(known_text_vectors):
        calculated_distance = calculate_distance(unknown_text_vector, element[1])
        if calculated_distance < distance:
            distance = calculated_distance
            label = language_labels[element[0]]
    return [label, distance]


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
            or not type_elements(unknown_text_vector, (int, float)) \
            or not type_elements(known_text_vector, (int, float)):
        return None
    distance = 0
    for element in enumerate(unknown_text_vector):
        distance += fabs(element[1] - known_text_vector[element[0]])
    return round(distance, 5)

def checking_types_language_knn(unknown_text_vector: list, known_text_vectors: list,
                                    language_labels: list) -> True or False:
    """
    Checks isinstance in predict_language_knn with isinstance()
    :param unknown_text_vector: list with int or float
    :param known_text_vectors: list with lists
    :param language_labels: string
    :return: True
    """
    texts = [unknown_text_vector, known_text_vectors, language_labels]
    types = [(int, float), list, str]
    for element in enumerate(texts):
        if not isinstance(element[1], list):
            return False
        if not type_elements(element[1], types[element[0]]):
            return False
    if len(known_text_vectors) != len(language_labels):
        return False
    return True


def min_distance_to_neighbour(dicts: list, label: str) -> float:
    """
    Calculates minimum distance in one label
    :param dicts: a dictionary
    :param label: a label
    """
    min_distance = 10
    for i in dicts:
        if label == i['label']:
            if i['distance'] < min_distance:
                min_distance = i['distance']
    return min_distance


def find_freq_label(labels_count: dict, dicts: list) -> str:
    """
    Detects the most frequent label in labels_count
    :param labels_count: dict with label:count
    :param dicts: list with dict
    """
    min_distance = 0
    freq_label = ''
    for key in labels_count:
        if labels_count[key] > min_distance:
            min_distance = labels_count[key]
            freq_label = key
        if labels_count[key] == min_distance:
            if min_distance_to_neighbour(dicts, key) \
                    < min_distance_to_neighbour(dicts, freq_label):
                freq_label = key
    return freq_label


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
    if not checking_types_language_knn(unknown_text_vector, known_text_vectors,
                                    language_labels):
        return None
    distances = []
    dicts = []
    if metric == 'manhattan':
        for vector in known_text_vectors:
            distances.append(calculate_distance_manhattan(unknown_text_vector, vector))
    elif metric == 'euclid':
        for vector in known_text_vectors:
            distances.append(calculate_distance(unknown_text_vector, vector))
    else:
        return None
    for element in enumerate(distances):
        dicts.append({'label':language_labels[element[0]], 'distance': element[1]})
    dicts = sorted(dicts, key=lambda x: x['distance'])
    dicts = dicts[:k]
    labels_count = {}
    for i in dicts:
        if i['label'] in labels_count:
            labels_count[i['label']] += 1
        else:
            labels_count[i['label']] = 1
    freq_label = find_freq_label(labels_count, dicts)
    return [freq_label, dicts[0]['distance']]


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
