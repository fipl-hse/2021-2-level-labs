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
    freq_dict = {}
    # go through the list of tokens, make a dict, where token is a key, and the number of times
    # it appears in the list is the value
    for i in tokens:
        if i in freq_dict.keys() and isinstance(i, str):
            freq_dict[i] += 1
        elif i not in freq_dict.keys() and isinstance(i, str):
            freq_dict[i] = 1
        else:
            return None
    # make a frequency dict: for every key set new value: the number of times the token appears divided
    # on the length of the tokens list
    for key, value in freq_dict.items():
        freq_dict[key] = round(value / len(tokens), 5)
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
    if any(not isinstance(i, list) for i in texts_corpus) or any(not isinstance(j, str) for j in language_labels):
        return None
    language_profiles = {}
    lang_index = 0
    # iterate through the text_corpus, apply get_freq_dict function to every element, add to language_profiles a pair:
    # key - language from language_labels, value - frequency dictionary
    for item in texts_corpus:
        freq_dict = get_freq_dict(item)
        language_profiles[language_labels[lang_index]] = freq_dict
        lang_index += 1
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) or len(language_profiles) == 0:
        return None
    features = []
    # get the list of unique words from every profile, add them to the common feature list
    for item in language_profiles.values():
        features.extend(list(item.keys()))
    # return features sorted in alphabetical order
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
    # get language features (function get_language_features applied)
    language_features = get_language_features(language_profiles)
    text_vector = []
    # create text vector
    for item in language_features:
        if item in original_text:
            max_value = 0
            for i in language_profiles.values():
                if item in i.keys() and i[item] > max_value:
                    max_value = i[item]
                else:
                    continue
            text_vector.append(max_value)
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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    if any(not isinstance(i, (int, float)) for i in unknown_text_vector) or \
            any(not isinstance(j, (int, float)) for j in known_text_vector):
        return None
    sum_of_distances = 0
    # iterate through unknown_text_vector and known_text_vector values, apply euclid metric
    for i in range(len(unknown_text_vector)):
        sum_of_distances += (unknown_text_vector[i] - known_text_vector[i]) ** 2
    return round(sum_of_distances ** 0.5, 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) or len(language_labels) != len(known_text_vectors):
        return None
    if any(not isinstance(i, (int, float)) for i in unknown_text_vector) or \
            any(not isinstance(j, list) for j in known_text_vectors) \
            or any(not isinstance(s, str) for s in language_labels):
        return None
    all_distances = []
    # get nested list of all distances. Inner list: [language label, distance]
    for i in range(len(known_text_vectors)):
        all_distances.append([language_labels[i], calculate_distance(unknown_text_vector, known_text_vectors[i])])
    # sort the list by distance (from smallest to biggest)
    distances = sorted(all_distances, key=lambda x: x[1])
    # get the element with the smallest distance
    return distances[0]


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    if any(not isinstance(i, (int, float)) for i in unknown_text_vector) or \
            any(not isinstance(j, (int, float)) for j in known_text_vector):
        return None
    distance_manhattan = 0
    # calculate distance by manhattan metric
    for i in range(len(unknown_text_vector)):
        distance_manhattan += abs(unknown_text_vector[i] - known_text_vector[i])
    return round(distance_manhattan, 2)


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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) or len(language_labels) != len(known_text_vectors) \
            or not isinstance(k, int) or metric not in ['manhattan', 'euclid']:
        return None
    if any(not isinstance(i, (int, float)) for i in unknown_text_vector) or \
            any(not isinstance(j, list) for j in known_text_vectors) \
            or any(not isinstance(s, str) for s in language_labels):
        return None

    # get the list of distances
    distance_list = []
    for i in range(len(known_text_vectors)):
        if metric == 'euclid':
            distance_list.append([language_labels[i], calculate_distance(unknown_text_vector, known_text_vectors[i])])
        elif metric == 'manhattan':
            distance_list.append(
                [language_labels[i], calculate_distance_manhattan(unknown_text_vector, known_text_vectors[i])])
    distances = sorted(distance_list, key=lambda x: x[1])[:k]

    # get the dict with language label: number of times this label is present in the distances
    predicted_languages = {}
    for j in range(len(distances)):
        if distances[j][0] in predicted_languages:
            predicted_languages[distances[j][0]] += 1
        else:
            predicted_languages[distances[j][0]] = 1

    # get the most frequent language in the list of distances
    max_match = 0
    best_match_language = ""
    for key, value in predicted_languages.items():
        if value > max_match:
            max_match = value
            best_match_language = key

    # return the result
    if max_match == 1:
        return distances[0]
    else:
        return [best_match_language, distances[0][1]]


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
    # get regular text vector
    text_vector = get_text_vector(original_text, language_profiles)
    sparse_vector = []
    count = 0
    # iterate through the regular text vector. When non-zero value met, append to sparse_vector the list:
    # [index of non-zero value, non-zero value]
    for i in text_vector:
        if i == 0:
            count += 1
            continue
        else:
            sparse_vector.append([count, i])
            count += 1
    return sparse_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    if any(not isinstance(i, list) for i in unknown_text_vector) or \
            any(not isinstance(j, list) for j in known_text_vector):
        return None
    sum_of_distances = 0

    # make vectors dicts, with the index of non-zero values as keys and the non-zero values as values
    unknown_text_vector = dict(unknown_text_vector)
    known_text_vector = dict(known_text_vector)
    for key, value in unknown_text_vector.items():
        if key in known_text_vector.keys():
            # apply euclid metric to non-zero elements at the same indexes of 2 vectors
            sum_of_distances += (unknown_text_vector[key] - known_text_vector[key]) ** 2
            # delete the element from known_text_vector to avoid counting it for the 2d time
            del known_text_vector[key]
        else:
            # apply euclid metric to non-zero element of unknown_text_vector element
            # where known_text_vector has zero at this index or no element with such index
            sum_of_distances += unknown_text_vector[key] ** 2
    if len(known_text_vector):
        # apply euclid metric to non-zero element of known_text_vector element
        # where unknown_text_vector had zero at this index or no element with such index
        for value in known_text_vector.values():
            sum_of_distances += value ** 2
    return round(sum_of_distances ** 0.5, 5)


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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) or len(language_labels) != len(known_text_vectors) \
            or not isinstance(k, int):
        return None
    if any(not isinstance(i, list) for i in unknown_text_vector) or \
            any(not isinstance(j, list) for j in known_text_vectors) \
            or any(not isinstance(s, str) for s in language_labels):
        return None

    # get the list of distances
    distance_list = []
    for i in range(len(known_text_vectors)):
        distance_list.append(
            [language_labels[i], calculate_distance_sparse(unknown_text_vector, known_text_vectors[i])])
    distances = sorted(distance_list, key=lambda x: x[1])[:k]

    # get the dict with language label: number of times this label is present in the distances
    predicted_languages = {}
    for j in range(len(distances)):
        if distances[j][0] in predicted_languages:
            predicted_languages[distances[j][0]] += 1
        else:
            predicted_languages[distances[j][0]] = 1

    # get the most frequent language in the list of distances
    max_match = 0
    best_match_language = ""
    for key, value in predicted_languages.items():
        if value > max_match:
            max_match = value
            best_match_language = key

    # return the result
    if max_match == 1:
        return distances[0]
    else:
        return [best_match_language, distances[0][1]]
