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
    for token in tokens:
        if not isinstance(token, str):
            return None
    freq_dict = {}
    for token in tokens:
        if token not in freq_dict:
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1
    for token in freq_dict:
        freq_dict[token] = round(freq_dict[token] / len(tokens), 5)
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
    frequences = []
    for word in get_language_features(language_profiles):
        if word in original_text:
            for freq_dict in language_profiles.values():
                if word in freq_dict.keys():
                    frequences.append(freq_dict[word])
            text_vector.append(max(frequences))
            frequences = []
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
    for number in unknown_text_vector:
        if not isinstance(number, int) and not isinstance(number, float):
            return None
    for number in known_text_vector:
        if not isinstance(number, int) and not isinstance(number, float):
            return None
    distance = 0
    for num_unk, num_kn in zip(unknown_text_vector, known_text_vector):
        distance += (num_unk-num_kn)**2
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
    for number in unknown_text_vector:
        if not isinstance(number, (float, int)):
            return None
    for number in known_text_vectors:
        if not isinstance(number, list):
            return None
    for label in language_labels:
        if not isinstance(label, str):
            return None
    dictionary = {}
    for ind, element in enumerate(known_text_vectors):
        dictionary[language_labels[ind]] = calculate_distance(unknown_text_vector, element)
    return [min(dictionary, key=dictionary.get), min(dictionary.values())]


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list)\
            or not isinstance(known_text_vector, list):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, int) and not isinstance(number, float):
            return None
    for number in known_text_vector:
        if not isinstance(number, int) and not isinstance(number, float):
            return None
    distance = 0
    for num_unk, num_kn in zip(unknown_text_vector, known_text_vector):
        distance += abs(num_unk-num_kn)
    return round(distance, 5)

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
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vectors, list)
            or not isinstance(language_labels, list)
            or not isinstance(k, int)
            or not isinstance(metric, str)):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, int) and not isinstance(number, float):
            return None
    distances = []
    if metric == 'euclid':
        for vector in known_text_vectors:
            distances.append(calculate_distance(unknown_text_vector, vector))
    else:
        for vector in known_text_vectors:
            distances.append(calculate_distance_manhattan(unknown_text_vector, vector))
    closest_languages = sorted(zip(language_labels, distances), key=lambda x: x[1])[:k]
    language_dict = {}
    for element in closest_languages:
        if element[0] not in language_dict:
            language_dict[element[0]] = 1
        else:
            language_dict[element[0]] += 1
    result = [max(language_dict, key=language_dict.get), min(distances)]
    return result

# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or not isinstance(language_profiles, dict):
        return None
    text_vector = []
    frequences = []
    for word in get_language_features(language_profiles):
        if word in original_text:
            for freq_dict in language_profiles.values():
                if word in freq_dict.keys():
                    frequences.append(freq_dict[word])
            text_vector.append(max(frequences))
            frequences = []
        else:
            text_vector.append(0)
    if not text_vector:
        return None
    sparce_vector = []
    for i, number in enumerate(text_vector):
        if number != 0:
            sparce_vector.append([i, number])
    return sparce_vector

def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not isinstance(unknown_text_vector, list)\
            or not isinstance(known_text_vector, list):
        return None
    for element in unknown_text_vector:
        if not isinstance(element, list):
            return None
    for element in known_text_vector:
        if not isinstance(element, list):
            return None
    distance = 0
    dictionary = {}
    for element in unknown_text_vector:
        dictionary[element[0]] = element[1]
    for element in known_text_vector:
        if element[0] not in dictionary:
            dictionary[element[0]] = element[1]
        else:
            dictionary[element[0]] -= element[1]
    for value in dictionary.values():
        distance += value**2
    return round(distance**0.5, 5)


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
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vectors, list)
            or not isinstance(language_labels, list)
            or not isinstance(k, int)):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    distances = []
    for vector in known_text_vectors:
        distances.append(calculate_distance_sparse(unknown_text_vector, vector))
    closest_languages = sorted(zip(language_labels, distances), key=lambda x: x[1])[:k]
    language_dict = {}
    for element in closest_languages:
        if element[0] not in language_dict:
            language_dict[element[0]] = 1
        else:
            language_dict[element[0]] += 1
    result = [max(language_dict, key=language_dict.get), min(distances)]
    return result
