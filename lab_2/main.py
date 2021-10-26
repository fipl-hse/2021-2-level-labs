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
    for word in tokens:
        if not isinstance(word, str):
            return None
        if word not in freq_dict:
            freq_dict[word] = round(tokens.count(word) / len(tokens), 5)
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
    for lang in language_labels:
        if not isinstance(lang, str):
            return None
    for tokens in texts_corpus:
        if not isinstance(tokens, list):
            return None
    for element, lang in enumerate(language_labels):
        language_profiles[lang] = get_freq_dict(texts_corpus[element])
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) or not language_profiles.items():
        return None
    for all_keys in language_profiles.keys():
        if not isinstance(all_keys, str):
            return None
    for all_values in language_profiles.values():
        if not isinstance(all_values, dict):
            return None
    features = []
    for lang in language_profiles.values():
        for word in lang:
            if word not in features:
                features.append(word)
    return sorted(features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) or not language_profiles.items() \
            or not isinstance(original_text, list):
        return None
    for all_keys in language_profiles.keys():
        if not isinstance(all_keys, str):
            return None
    for all_values in language_profiles.values():
        if not isinstance(all_values, dict):
            return None
    text_vector = []
    lang_profile_freq = {}
    lang_features = get_language_features(language_profiles)
    for lang in language_profiles:
        lang_profile_freq.update(language_profiles.get(lang))
    for word_frequency in lang_features:
        if word_frequency in original_text:
            text_vector.append(lang_profile_freq.get(word_frequency))
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
    for bad_input1 in unknown_text_vector:
        if not isinstance(bad_input1, int) \
                and not isinstance(bad_input1, float):
            return None
    for bad_input2 in known_text_vector:
        if not isinstance(bad_input2, int) \
                and not isinstance(bad_input2, float):
            return None
    vector_distance = 0
    for i, frequency in enumerate(unknown_text_vector):
        vector_distance += ((frequency - known_text_vector[i]) ** 2)
    return round(vector_distance ** 0.5, 5)

def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list)\
        or not isinstance(known_text_vectors, list) \
        or not isinstance(language_labels, list) \
        or len(known_text_vectors) != len(language_labels):
        return None
    for bad_inputs1 in unknown_text_vector:
        if not isinstance(bad_inputs1, int) and not isinstance(bad_inputs1, float):
            return None
    for bad_inputs2 in known_text_vectors:
        for i in bad_inputs2:
            if not isinstance(i, int) and not isinstance(i, float):
                return None
    for bad_inputs3 in language_labels:
        if not isinstance(bad_inputs3, str):
            return None
    all_distances = []
    for vectors in known_text_vectors:
        all_distances.append(calculate_distance(unknown_text_vector, vectors))
    lang_vectors = {}
    for number, langs in enumerate(language_labels):
        lang_vectors[langs] = all_distances[number]
    for lang_label, all_vectors in lang_vectors.items():
        if all_vectors == min(lang_vectors.values()):
            vector_result = [lang_label, all_vectors]
    return vector_result


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vector, list)):
        return None
    for bad_input in unknown_text_vector:
        if not isinstance(bad_input, float) and not isinstance(bad_input, int):
            return None
    for bad_input1 in known_text_vector:
        if not isinstance(bad_input1, float) and not isinstance(bad_input1, int):
            return None
    manhattan_distance = 0
    for i, frequency in enumerate(unknown_text_vector):
        manhattan_distance += abs(frequency - known_text_vector[i])
    return round(manhattan_distance, 5)


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
    for bad_input in unknown_text_vector:
        if not isinstance(bad_input, int) and not isinstance(bad_input, float):
            return None
    if len(language_labels) != len(known_text_vectors):
        return None
    all_distances = []
    if metric == 'euclid':
        for all_vectors in known_text_vectors:
            all_distances.append(calculate_distance(unknown_text_vector, all_vectors))
    else:
        for all_vectors in known_text_vectors:
            all_distances.append(calculate_distance_manhattan
                                 (unknown_text_vector, all_vectors))
    k_distances = sorted(zip(language_labels, all_distances), key=lambda x: x[1])[:k]
    language_k_frequency = {}
    for knn in k_distances:
        if knn[0] not in language_k_frequency:
            language_k_frequency[knn[0]] = 1
        language_k_frequency[knn[0]] += 1
    return [max(language_k_frequency, key=language_k_frequency.get), min(all_distances)]

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
