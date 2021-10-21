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
    if not isinstance(tokens, list) or len(tokens) < 1:
        return None
    freq_dict = {}
    for token in tokens:
        if not isinstance(token, str):
            tokens.remove(token)
            return None
        if token not in freq_dict:
            freq_dict[token] = round(tokens.count(token) / len(tokens), 5)
    if len(freq_dict) == 0:
        return None
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
    if not isinstance(texts_corpus, list) or \
            not isinstance(language_labels, list):
        return None
    for num, label in enumerate(language_labels):
        if not isinstance(label, str):
            return None
        language_profiles[label] = get_freq_dict(texts_corpus[num])
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    features = []
    for key, val in language_profiles.items():
        if not isinstance(key, str) or\
                not isinstance(val, dict):
            return None
        for word, freq in val.items():
            if not isinstance(word, str) or\
                    not isinstance(freq, (int, float)):
                return None
            features.append(word)
    features = sorted(features)
    if len(features) == 0:
        return None
    return features


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or\
            not isinstance(language_profiles, dict):
        return None
    text_vector = []
    base = get_language_features(language_profiles)
    profiles = list(language_profiles.values())
    for word in base:
        if word in original_text:
            for profile in profiles:
                if word in profile:
                    text_vector.append(profile.get(word))
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
    if not isinstance(unknown_text_vector, list) or\
            not isinstance(known_text_vector, list):
        return None
    for unk in unknown_text_vector:
        if not isinstance(unk, (int, float)):
            return None
    for knwn in known_text_vector:
        if not isinstance(knwn, (int, float)):
            return None
    distance = 0
    for num, text in enumerate(unknown_text_vector):
        distance += (text - known_text_vector[num]) ** 2
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
    if not isinstance(unknown_text_vector, list) or\
            not isinstance(known_text_vectors, list) or\
            not isinstance(language_labels, list) or\
            len(language_labels) != len(known_text_vectors):
        return None
    for unk in unknown_text_vector:
        if not isinstance(unk, (int, float)):
            return None
    for label in language_labels:
        if not isinstance(label, str):
            return None
    distances = []
    for text in known_text_vectors:
        if not isinstance(text, list):
            return None
        for num in text:
            if not isinstance(num, (int, float)):
                return None
        distances.append(calculate_distance(unknown_text_vector, text))
    answer = min(distances)
    result = [language_labels[distances.index(answer)], answer]
    return result


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) or\
            not isinstance(known_text_vector, list):
        return None
    for kn_num in known_text_vector:
        if not isinstance(kn_num, (int, float)):
            return None
    for unk_num in unknown_text_vector:
        if not isinstance(unk_num, (int, float)):
            return None
    manhattan_distance = 0
    for num, unk_text in enumerate(unknown_text_vector):
        manhattan_distance += abs(unk_text - known_text_vector[num])
    manhattan_distance = round(manhattan_distance, 5)
    return manhattan_distance


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
    if not (isinstance(unknown_text_vector, list) and
            isinstance(known_text_vectors, list) and
            isinstance(language_labels, list) and
            isinstance(k, int) and
            isinstance(metric, str) and
            len(known_text_vectors) == len(language_labels)):
        return None
    for unk_num in unknown_text_vector:
        if not isinstance(unk_num, (int, float)):
            return None
    distances = []
    for text in known_text_vectors:
        if not isinstance(text, list):
            return None
        for kn_num in text:
            if not isinstance(kn_num, (int, float)):
                return None
        if metric == "manhattan":
            distances.append(calculate_distance_manhattan(unknown_text_vector, text))
        elif metric == "euclid":
            distances.append(calculate_distance(unknown_text_vector, text))
    norm_distances = sorted(distances)[:k]
    norm_labels = []
    for distance in norm_distances:
        norm_labels.append(language_labels[distances.index(distance)])
    norm_labels = sorted(zip(norm_labels, norm_distances), key=lambda x: x[1])
    closest_labels = {}
    for label, _ in norm_labels:
        if label not in closest_labels:
            closest_labels[label] = 0
        closest_labels[label] += 1
    return [max(closest_labels, key=closest_labels.get), min(norm_distances)]


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or\
            not isinstance(language_profiles, dict) or\
            not (isinstance(word, str) for word in original_text):
        return None
    features = get_language_features(language_profiles)
    if not isinstance(features, list):
        return None
    text_vector = []
    profiles = language_profiles.values()
    for word in features:
        if word in original_text:
            for profile in profiles:
                if word in profile:
                    text_vector.append([features.index(word), profile.get(word)])
    return text_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not isinstance(unknown_text_vector, list) or\
            not isinstance(known_text_vector, list):
        return None
    dict_unk = {}
    dict_knwn = {}
    for unk in unknown_text_vector:
        if not isinstance(unk, list) or\
                len(unk) != 2:
            return None
        dict_unk[unk[0]] = unk[1]
    for knwn in known_text_vector:
        if not isinstance(knwn, list) or\
                len(knwn) != 2:
            return None
        dict_knwn[knwn[0]] = knwn[1]
    max_len = len(dict_knwn) + len(dict_unk)
    distance = 0
    for num in range(max_len):
        if num in dict_unk and num in dict_knwn:
            distance += (dict_unk.get(num) - dict_knwn.get(num)) ** 2
        elif num in dict_unk and num not in dict_knwn:
            distance += dict_unk.get(num) ** 2
        elif num not in dict_unk and num in dict_knwn:
            distance += dict_knwn.get(num) ** 2
    distance = round(distance ** 0.5, 5)
    return distance


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
    if not (isinstance(unknown_text_vector, list) and
            isinstance(known_text_vectors, list) and
            isinstance(language_labels, list) and
            isinstance(k, int) and
            len(known_text_vectors) == len(language_labels)):
        return None
    for unk in unknown_text_vector:
        if not isinstance(unk, list) or\
                not isinstance(unk[0], int) or\
                not isinstance(unk[1], (int, float)):
            return None
    distances = []
    for knwn_text in known_text_vectors:
        if not isinstance(knwn_text, list):
            return None
        for knwn in knwn_text:
            if not isinstance(knwn, list) or\
                    not isinstance(knwn[0], int) or\
                    not isinstance(knwn[1], (int, float)):
                return None
        distances.append(calculate_distance_sparse(unknown_text_vector, knwn_text))
    norm_distances = sorted(distances)[:k]
    norm_labels = []
    for distance in norm_distances:
        norm_labels.append(language_labels[distances.index(distance)])
    norm_labels = sorted(zip(norm_labels, norm_distances), key=lambda x: x[1])
    closest_labels = {}
    for label, _ in norm_labels:
        if label not in closest_labels:
            closest_labels[label] = 0
        closest_labels[label] += 1
    return [max(closest_labels, key=closest_labels.get), min(norm_distances)]