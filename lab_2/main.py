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
    for token in tokens:
        if token not in freq_dict:
            freq_dict[token] = round(tokens.count(token) / len(tokens), 5)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not (
        isinstance(texts_corpus, list)
        and all(isinstance(l, list) for l in texts_corpus)
        and isinstance(language_labels, list)
        and all(isinstance(s, str) for s in language_labels)
        ):
        return None
    language_profiles = {}
    for index, lang in enumerate(language_labels):
        language_profiles[lang] = get_freq_dict(texts_corpus[index])
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (
        isinstance(language_profiles, dict)
        and language_profiles != {}
        and all(isinstance(s, str) for s in language_profiles)
        and all(isinstance(d, dict) for d in language_profiles.values())
        ):
        return None
    lang_features = []
    for freq_dict in language_profiles.values():
        for token in freq_dict:
            if token not in lang_features:
                lang_features.append(token)
    lang_features.sort()
    return lang_features


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (
        isinstance(original_text, list)
        and all(isinstance(s, str) for s in original_text)
        and isinstance(language_profiles, dict)
        and language_profiles != {}
        and all(isinstance(s, str) for s in language_profiles)
        and all(isinstance(d, dict) for d in language_profiles.values())
        ):
        return None
    lang_profiles_mix = {}
    for freq_dict in language_profiles.values():
        for index, token in freq_dict.items():
            if token > lang_profiles_mix.get(index, 0):
                    lang_profiles_mix[index] = token
    lang_features = get_language_features(language_profiles)
    text_vector = []
    for feature in lang_features:
        if feature in original_text:
            text_vector.append(lang_profiles_mix[feature])
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
    if not (
        isinstance(unknown_text_vector, list)
        and all(isinstance(n, (int, float)) for n in unknown_text_vector)
        and isinstance(known_text_vector, list)
        and all(isinstance(m, (int, float)) for m in known_text_vector)
        ):
        return None
    distance = 0
    for i in range(len(unknown_text_vector)):
        distance += ((unknown_text_vector[i] - known_text_vector[i])**2)
    distance = round(distance**0.5, 5)
    return distance


def predict_language_score(unknown_text_vector: list, known_text_vectors: list, language_labels: list) ->  [str, int] or None:
    if not (
        isinstance(unknown_text_vector, list)
        and all(isinstance(n, (int, float)) for n in unknown_text_vector)
        and isinstance(known_text_vectors, list)
        and all(isinstance(m, list) for m in known_text_vectors)
        and isinstance(language_labels, list)
        and all(isinstance(s, str) for s in language_labels)
        and len(known_text_vectors) == len(language_labels)
        ):
        return None
    distances = []
    for known_text_vector in known_text_vectors:
        distance = calculate_distance(unknown_text_vector, known_text_vector)
        distances.append(distance)
    minimum = min(distances)
    score = [language_labels[distances.index(minimum)], minimum]
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
    for i in range(len(unknown_text_vector)):
        distance += abs(unknown_text_vector[i] - known_text_vector[i])
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
    if not (
        isinstance(unknown_text_vector, list)
        and all(isinstance(n, (int, float)) for n in unknown_text_vector)
        and isinstance(known_text_vectors, list)
        and all(isinstance(m, list) for m in known_text_vectors)
        and isinstance(language_labels, list)
        and all(isinstance(s, str) for s in language_labels)
        and len(known_text_vectors) == len(language_labels)
        ):
        return None
    if metric == 'euclid':
        calc_dist = calculate_distance
    elif metric == 'manhattan':
        calc_dist = calculate_distance_manhattan
    distances = []
    for known_text_vector in known_text_vectors:
        distance = calc_dist(unknown_text_vector, known_text_vector)
        distances.append(distance)
    sorted_distances = (sorted(distances))[:k]
    langs = []
    for i in sorted_distances:
        index = distances.index(i)
        langs.append(language_labels[index])
    langs_counter = {}
    for l in set(langs):
        langs_counter[l] = langs.count(l)
    knn_predict = [max(langs_counter, key=langs_counter.get), min(sorted_distances)]
    return knn_predict


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (
        isinstance(original_text, list)
        and all(isinstance(s, str) for s in original_text)
        and isinstance(language_profiles, dict)
        and language_profiles != {}
        and all(isinstance(s, str) for s in language_profiles)
        and all(isinstance(d, dict) for d in language_profiles.values())
        ):
        return None
    lang_profiles_mix = {}
    for freq_dict in language_profiles.values():
        for index, token in freq_dict.items():
            if token > lang_profiles_mix.get(index, 0):
                    lang_profiles_mix[index] = token
    lang_features = get_language_features(language_profiles)
    text_vector_standard = []
    for feature in lang_features:
        if feature in original_text:
            text_vector_standard.append(lang_profiles_mix[feature])
        else:
            text_vector_standard.append(0)
    text_vector_sparse = []
    for i, v in enumerate(text_vector_standard):
        if v != 0:
            text_vector_sparse.append([i, v])
    return text_vector_sparse


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not (
        isinstance(unknown_text_vector, list)
        and all(isinstance(n, (list)) for n in unknown_text_vector)
        and isinstance(known_text_vector, list)
        and all(isinstance(m, (list)) for m in known_text_vector)
        ):
        return None
    unknown_text_dict = dict(unknown_text_vector)
    known_text_dict = dict(known_text_vector)
    dict_mix = unknown_text_dict.copy()
    for k, v in known_text_dict.items():
        if k not in dict_mix:
            dict_mix[k] = v
        else:
            dict_mix[k] = dict_mix[k] - known_text_dict[k]
    distance = 0
    for v in dict_mix.values():
        distance += v**2
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
    if not (
        isinstance(unknown_text_vector, list)
        and all(isinstance(n, list) for n in unknown_text_vector)
        and isinstance(known_text_vectors, list)
        and all(isinstance(m, list) for m in known_text_vectors)
        and isinstance(language_labels, list)
        and all(isinstance(s, str) for s in language_labels)
        and len(known_text_vectors) == len(language_labels)
        ):
        return None
    distances = []
    for known_text_vector in known_text_vectors:
        distance = calculate_distance_sparse(unknown_text_vector, known_text_vector)
        distances.append(distance)
    sorted_distances = (sorted(distances))[:k]
    langs = []
    for i in sorted_distances:
        index = distances.index(i)
        langs.append(language_labels[index])
    langs_counter = {}
    for l in set(langs):
        langs_counter[l] = langs.count(l)
    knn_predict = [max(langs_counter, key=langs_counter.get), min(sorted_distances)]
    return knn_predict
