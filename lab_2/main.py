"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words


def list_elements_isinstance(this_list: list, this_type: type) -> bool:
    """
    Checks elements' types in a list - saves space
    :param this_list: any list
    :param this_type: any type
    :return: true if the list contains elements of only this_type
    """
    for element in this_list:
        if not isinstance(element, this_type):
            return False

    return True


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

        if token in freq_dict.keys():
            freq_dict[token] = freq_dict[token] + 1
        else:
            freq_dict[token] = 1

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

    language_profiles = {}

    for index, language_label in enumerate(language_labels):
        if not isinstance(language_label, str) or not isinstance(texts_corpus[index], list):
            return None

        language_profiles[language_label] = get_freq_dict(texts_corpus[index])

    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if not isinstance(language_profiles, dict) or not language_profiles:
        return None

    all_words = []

    for language_profile in language_profiles.keys():
        for word in language_profiles[language_profile].keys():
            if word in all_words:
                all_words.remove(word)
            else:
                all_words.append(word)

    all_words.sort()

    return all_words


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if not isinstance(language_profiles, dict) or not language_profiles\
            or not isinstance(original_text, list):
        return None

    for word in original_text:
        if not isinstance(word, str):
            return None

    text_vector = []

    unique_words = get_language_features(language_profiles)

    for word in unique_words:
        if word in original_text:
            text_vector.append(get_word_freq_value(word, language_profiles))
        else:
            text_vector.append(0)

    return text_vector


def get_word_freq_value(word: str, language_profiles: dict) -> float or int:
    """
    Returns word frequency from multiple given language profiles
    :param word: given word
    :param language_profiles: a dictionary of dictionaries - language profiles
    :return: word frequency
    """

    freq_value = 0

    for language_profile in language_profiles:
        if word in language_profiles[language_profile]:
            if language_profiles[language_profile][word] > freq_value:
                freq_value = language_profiles[language_profile][word]

    return freq_value


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """

    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list)\
            or not list_elements_isinstance(unknown_text_vector, (int, float))\
            or not list_elements_isinstance(known_text_vector, (int, float)):
        return None

    distance = 0

    for index in range(len(unknown_text_vector)):
        distance += pow(unknown_text_vector[index] - known_text_vector[index], 2)

    return round(pow(distance, 1/2), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """

    if not isinstance(unknown_text_vector, list) or not isinstance(unknown_text_vector, list)\
            or not isinstance(language_labels, list) \
            or not list_elements_isinstance(unknown_text_vector, (int, float))\
            or not list_elements_isinstance(known_text_vectors, list)\
            or not list_elements_isinstance(language_labels, str):
        return None

    if len(language_labels) != len(known_text_vectors):
        return None

    result_language_score = []

    for index, known_text_vector in enumerate(known_text_vectors):
        distance = calculate_distance(unknown_text_vector, known_text_vector)
        if not result_language_score:
            result_language_score = [language_labels[index], distance]
        else:
            if distance < result_language_score[1]:
                result_language_score = [language_labels[index], distance]

    return result_language_score


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """

    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list) \
            or not list_elements_isinstance(unknown_text_vector, (int, float)) \
            or not list_elements_isinstance(known_text_vector, (int, float)):
        return None

    distance = 0

    for index in range(len(unknown_text_vector)):
        distance += abs(unknown_text_vector[index] - known_text_vector[index])

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

    if not isinstance(unknown_text_vector, list) or not isinstance(unknown_text_vector, list)\
            or not isinstance(language_labels, list)\
            or not isinstance(k, int)\
            or not isinstance(metric, str)\
            or not list_elements_isinstance(unknown_text_vector, (int, float))\
            or not list_elements_isinstance(known_text_vectors, list)\
            or not list_elements_isinstance(language_labels, str):
        return None

    if len(language_labels) != len(known_text_vectors):
        return None

    nearest_language_distances = []

    for index, known_text_vector in enumerate(known_text_vectors):
        if metric == 'manhattan':
            nearest_language_distances.append(
                [language_labels[index], calculate_distance_manhattan(unknown_text_vector, known_text_vector)])
        else:
            nearest_language_distances.append(
                [language_labels[index], calculate_distance(unknown_text_vector, known_text_vector)])

    nearest_language_distances.sort(key=lambda x: x[1])
    nearest_language_distances = nearest_language_distances[:k]

    results_freq_dict = {}

    for index, nearest_language_distance in enumerate(nearest_language_distances):
        if nearest_language_distance[0] not in results_freq_dict.keys():
            results_freq_dict[nearest_language_distance[0]] = 1
        else:
            results_freq_dict[nearest_language_distance[0]] += 1

    highest_results = []

    for result_freq in results_freq_dict:
        if not highest_results:
            highest_results = [[result_freq, results_freq_dict[result_freq]]]
        elif results_freq_dict[result_freq] > highest_results[0][1]:
            highest_results = [[result_freq, results_freq_dict[result_freq]]]
        elif results_freq_dict[result_freq] == highest_results[0][1]:
            highest_results.append([result_freq, results_freq_dict[result_freq]])

    highest_results_labels = [highest_result[0] for highest_result in highest_results]

    for nearest_language_distance in nearest_language_distances:
        if nearest_language_distance[0] in highest_results_labels:
            return [nearest_language_distance[0], nearest_language_distances[0][1]]


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if not isinstance(language_profiles, dict) or not language_profiles \
            or not isinstance(original_text, list):
        return None

    for word in original_text:
        if not isinstance(word, str):
            return None

    text_vector = []

    unique_words = get_language_features(language_profiles)

    for index, word in enumerate(unique_words):
        if word in original_text:
            text_vector.append([index, get_word_freq_value(word, language_profiles)])

    return text_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """

    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list)\
            or not list_elements_isinstance(unknown_text_vector, list)\
            or not list_elements_isinstance(known_text_vector, list):
        return None

    distance = 0

    unknown_text_vector_dict = dict(unknown_text_vector)

    for element in known_text_vector:
        index = element[0]
        value = element[1]

        if index not in unknown_text_vector_dict.keys():
            unknown_text_vector_dict[index] = value
        else:
            unknown_text_vector_dict[index] -= value

    for element in unknown_text_vector_dict.values():
        distance += pow(element, 2)

    return round(pow(distance, 1/2), 5)


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

    if not isinstance(unknown_text_vector, list) or not isinstance(unknown_text_vector, list)\
            or not isinstance(language_labels, list)\
            or not isinstance(k, int)\
            or not list_elements_isinstance(unknown_text_vector, list)\
            or not list_elements_isinstance(known_text_vectors, list)\
            or not list_elements_isinstance(language_labels, str):
        return None

    if len(language_labels) != len(known_text_vectors):
        return None

    nearest_language_distances = []

    for index, known_text_vector in enumerate(known_text_vectors):
        nearest_language_distances.append(
            [language_labels[index], calculate_distance_sparse(unknown_text_vector, known_text_vector)])

    nearest_language_distances.sort(key=lambda x: x[1])
    nearest_language_distances = nearest_language_distances[:k]

    results_freq_dict = {}

    for index, nearest_language_distance in enumerate(nearest_language_distances):
        if nearest_language_distance[0] not in results_freq_dict.keys():
            results_freq_dict[nearest_language_distance[0]] = 1
        else:
            results_freq_dict[nearest_language_distance[0]] += 1

    highest_results = []

    for result_freq in results_freq_dict:
        if not highest_results:
            highest_results = [[result_freq, results_freq_dict[result_freq]]]
        elif results_freq_dict[result_freq] > highest_results[0][1]:
            highest_results = [[result_freq, results_freq_dict[result_freq]]]
        elif results_freq_dict[result_freq] == highest_results[0][1]:
            highest_results.append([result_freq, results_freq_dict[result_freq]])

    highest_results_labels = [highest_result[0] for highest_result in highest_results]

    for nearest_language_distance in nearest_language_distances:
        if nearest_language_distance[0] in highest_results_labels:
            return [nearest_language_distance[0], nearest_language_distances[0][1]]
