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
    pass

    if not isinstance(tokens, list) or None in tokens:
        return None
    frequency_dictionary = {}
    for word in tokens:
        frequency_dictionary[word] = round(tokens.count(word)/len(tokens), 5)
    return frequency_dictionary


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    pass

    if not isinstance(texts_corpus, list) or not isinstance(language_labels, list):
        return None
    if texts_corpus == [None] or language_labels == [None]:
        return None

    language_profiles = {}
    score = len(language_labels)
    for i in range(score):
        language_profiles[language_labels[i]] = texts_corpus[i]

    for key in language_profiles:
        language_profiles[key] = get_freq_dict(language_profiles[key])

    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    pass

    if not isinstance(language_profiles, dict) \
            or language_profiles == {}:
        return None
    uni_tok = []
    for freq_dict in language_profiles.values():
        uni_tok.extend(list(freq_dict.keys()))
    unique_tokens = sorted(uni_tok)
    return unique_tokens


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    pass

    if not isinstance(original_text, list) \
            or not isinstance(language_profiles, dict):
        return None
    text_vector = []
    text_features = get_language_features(language_profiles)
    for w in text_features:
        if w in original_text:
            for dictionary in language_profiles.values():
                if w in dictionary:
                    text_vector.append(dictionary[w])
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
    pass

    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vector, list):
        return None
    for num in unknown_text_vector:
        if not isinstance(num, (int, float)):
            return None
    for num in known_text_vector:
        if not isinstance(num, (int, float)):
            return None

    distance = 0
    score = len(unknown_text_vector)
    for i in range(score):
        step = unknown_text_vector[i] - known_text_vector[i]
        step = step ** 2
        distance += step

    distance = round(distance ** 0.5, 5)
    return distance


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    pass

    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or len(language_labels) != len(known_text_vectors):
        return None
    for num in unknown_text_vector:
        if not isinstance(num, (int, float)):
            return None
    for vector in known_text_vectors:
        if not isinstance(vector, list):
            return None
    for label in language_labels:
        if not isinstance(label, str):
            return None
    label_vector = {}
    for index, coordinate in enumerate(known_text_vectors):
        label_vector[language_labels[index]] = calculate_distance(unknown_text_vector, coordinate)
    result = ''
    for key, value in label_vector.items():
        if value == min(label_vector.values()):
            result = [key, value]
    return result


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    pass

    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vector, list):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, (int, float)):
            return None
    distance = 0
    for index, coordinate in enumerate(unknown_text_vector):
        distance += abs(coordinate - known_text_vector[index])
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

    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not isinstance(k, int) \
            or not isinstance(metric, str):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    distances = []
    for vector in known_text_vectors:
        if metric == 'euclid':
            distance = calculate_distance(unknown_text_vector, vector)
            distances.append(distance)
        elif metric == 'manhattam':
            distance = calculate_distance_manhattan(unknown_text_vector, vector)
            distances.append(distance)
    sorted_distances = sorted(distances)
    sorted_distances = sorted_distances[:k]
    labels = []
    for distance in sorted_distances:
        index_of_distance = distances.index(distance)
        if len(language_labels) == len(known_text_vectors):
            label = language_labels[index_of_distance]
            labels.append(label)
        else:
            return None
    dictionary_of_labels = {}
    for label in labels:
        if label in dictionary_of_labels:
            dictionary_of_labels[label] += 1
        else:
            dictionary_of_labels[label] = 1
    possible_label = max(dictionary_of_labels, key=dictionary_of_labels.get)
    possible_result = [possible_label, round(min(distances), 5)]
    return possible_result
