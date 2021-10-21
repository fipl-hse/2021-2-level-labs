"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words
import math

#4
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
        if not isinstance(token,str):
            return None
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    for token in freq_dict:
        freq_dict[token] = round(freq_dict[token]/len(tokens), 5)
    return freq_dict





def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not isinstance (texts_corpus, list) or not isinstance(language_labels, list):
        return None
    language_profiles = {}

    for index in texts_corpus:
        if not isinstance(index, list):
            return None
    for index in language_labels:
        if not isinstance(index, str):
            return None
    for index in range(len(language_labels)):
        language_profiles[language_labels[index]] = get_freq_dict(texts_corpus[index])
    return language_profiles
    



def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, list):
        return None
    unique_words = []
    for freq_dict in language_profiles.values():
        unique_words.extend(list(freq_dict.keys()))
    unique_words = sorted(unique_words)
    return  unique_words





def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(original_text, list) or isinstance(language_profiles, list)):
        return None
    text_vector = []
    for unique_words in get_language_features(language_profiles):
        if unique_words in original_text:
            for freq_dict in language_profiles.values():
                if unique_words in freq_dict:
                    text_vector.append(freq_dict[unique_words])
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
    if not (isinstance(unknown_text_vector, list) or isinstance(known_text_vector, list)):
        return None
    for element in unknown_text_vector:
        if not isinstance(element, (float, int)):
            return None
    for element in known_text_vector:
        if not isinstance(element, (float, int)):
            return None
    distance = 0
    for index, number in enumerate(unknown_text_vector):
        distance += (number - known_text_vector[index])**2
        distance = round(math.sqrt(distance), 5)
    return distance




def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not (isinstance(unknown_text_vector, list) or isinstance(known_text_vectors, list) or isinstance(language_labels, list)):
        return None
    for element in unknown_text_vector:
        if not isinstance(element, (float,int)):
            return None
    for vector in known_text_vectors:
        if not isinstance(vector, list):
            return None
    for label in language_labels:
        if not isinstance(label,str):
            return None
    if len(known_text_vectors) != len(language_labels):
        return None

    distance = []
    for vector in known_text_vectors:
        distance.append(calculate_distance(unknown_text_vector, vector))
    result_language_score = [language_labels[distance.index(min(distance))], min(distance)]
    return result_language_score

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
