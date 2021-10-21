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
    if not (
            isinstance(tokens, list)
            and all(isinstance(s, str) for s in tokens)
    ):
        return None
    freq_dict = {}
    length = len(tokens)
    for token in tokens:
        if token not in freq_dict:
            freq_dict[token] = round(tokens.count(token) / length, 5)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    language_profiles = {}
    if (not isinstance(texts_corpus, list)) or (not isinstance(language_labels, list)):
        return None
    for corpus, label in zip(texts_corpus, language_labels):
        if isinstance(corpus, str) or isinstance(label, str):
            language_profiles[label] = get_freq_dict(corpus)
        else:
            return None
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) or not language_profiles:
        return None
    unique_words = []
    for value in language_profiles.values():
        for value_1 in value:
            if value_1 not in unique_words:
                unique_words.append(value_1)
    unique_words.sort()
    return unique_words


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or not isinstance(language_profiles, dict):
        return None
    vector = []
    unique_words = get_language_features(language_profiles)
    max_word_freq = {}
    for word in unique_words:
        word_freq_value = 0
        for language_profile in language_profiles.keys():
            if language_profiles[language_profile].get(word, 0) > word_freq_value:
                word_freq_value = language_profiles[language_profile].get(word, 0)
        max_word_freq[word] = word_freq_value
    for token in unique_words:
        if token in original_text:
            vector.append(max_word_freq[token])
        else:
            vector.append(0)
    return vector


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vector, list)):
        return None

    for num in unknown_text_vector:
        if not isinstance(num, (int, float)):
            return None
    for num in known_text_vector:
        if not isinstance(num, (int, float)):
            return None
    distance = 0
    for index, coordinate in enumerate(unknown_text_vector):
        distance += ((coordinate - known_text_vector[index]) ** 2)
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
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list):
        return None
    for vector in known_text_vectors:
        if not isinstance(vector, list):
            return None
    if len(language_labels) != len(known_text_vectors):
        return None
    distances = []
    for known_text_vector in known_text_vectors:
        distance = calculate_distance(unknown_text_vector, known_text_vector)
        distances.append(distance)
    min_distance = min(distances)
    score = [language_labels[distances.index(min_distance)], min_distance]
    return score


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not (
            isinstance(unknown_text_vector, list)
            and all(isinstance(n, (int, float)) for n in unknown_text_vector)
            and isinstance(known_text_vector, list)
            and all(isinstance(m, (int, float)) for m in known_text_vector)
    ):
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
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vectors, list)
            or not isinstance(language_labels, list)):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, (float, int)):
            return None
    distances = []
    if metric == 'manhattan':
        for known_text_vector in known_text_vectors:
            distances.append(calculate_distance_manhattan(unknown_text_vector, known_text_vector))
    elif metric == 'euclid':
        for known_text_vector in known_text_vectors:
            distances.append(calculate_distance(unknown_text_vector, known_text_vector))
    nearest_languages = sorted(list(zip(language_labels, distances)))[:k]
    if not isinstance(nearest_languages, list):
        return None
    count_languages = {}
    for language in nearest_languages:
        if language not in count_languages:
            count_languages[language] = 1
        else:
            count_languages[language] += 1
    biggest_value = max(count_languages, key=count_languages.get)
    predicted_language = [biggest_value[0], round(min(distances), 5)]
    return predicted_language


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if (not isinstance(original_text, list)
            or not isinstance(language_profiles, dict)):
        return None
    text_vector = []
    for feature in get_language_features(language_profiles):
        if feature in original_text:
            for freq_dictionary in language_profiles.values():
                if feature in freq_dictionary:
                    text_vector.append([(get_language_features(language_profiles)).index(feature),
                                        freq_dictionary[feature]])
    return text_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    for unknown_vector in unknown_text_vector:
        if not isinstance(unknown_vector, list):
            return None
    for known_vector in known_text_vector:
        if not isinstance(known_vector, list):
            return None
    unknown_text_dict = dict(unknown_text_vector)
    known_text_dict = dict(known_text_vector)
    dict_mix = unknown_text_dict.copy()
    for key, value in known_text_dict.items():
        if key not in dict_mix:
            dict_mix[key] = value
        else:
            dict_mix[key] = dict_mix[key] - known_text_dict[key]
    distance = 0
    for value in dict_mix.values():
        distance += value ** 2
    return round(distance ** 0.5, 5)


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
            or not isinstance(language_labels, list) or not isinstance(k, int):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    distances = []
    for known_text_vector in known_text_vectors:
        distances.append(calculate_distance_sparse(unknown_text_vector, known_text_vector))
    nearest_languages = sorted(zip(language_labels, distances))[:k]
    count = {}
    for language in nearest_languages:
        if language[0] not in count:
            count[language[0]] = 1
        else:
            count[language[0]] += 1
    biggest_value = max(count, key=count.get)
    predicted_language = [biggest_value, min(distances)]
    return predicted_language
