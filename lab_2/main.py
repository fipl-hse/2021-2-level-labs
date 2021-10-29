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
    if not isinstance(tokens, list) or tokens == [None]:
        return None

    freqs = dict.fromkeys(tokens, float(0.0))

    for key in freqs:
        for i in tokens:
            if i == key:
                freqs[key] += 1

    for key in freqs:
        freqs[key] = round(freqs[key] / len(tokens), 5)

    return freqs


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
    if texts_corpus == [None] or language_labels == [None]:
        return None

    language_profiles = {}
    count = len(language_labels)
    for i in range(count):
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
    if not isinstance(language_profiles, dict) or language_profiles == {}:
        return None

    lang_feats = []

    for lang in language_profiles:
        temp = language_profiles[lang]
        new_keys = list(temp.keys())
        lang_feats += new_keys
        print(lang_feats)

    lang_feats = sorted(lang_feats)

    return lang_feats


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
    feats = get_language_features(language_profiles)
    feats_dict = {}

    for i in language_profiles:
        prof = language_profiles[i]
        for key in prof:
            if key in feats:
                feats_dict[key] = prof[key]

    for i in feats:
        if i in original_text:
            vector.append(feats_dict[i])
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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    if unknown_text_vector == [None] or known_text_vector == [None]:
        return None

    distance = 0.0

    count = len(unknown_text_vector)
    for i in range(count):
        temp = unknown_text_vector[i] - known_text_vector[i]
        temp = temp ** 2
        distance += temp

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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list):
        return None
    if not isinstance(language_labels, list):
        return None
    if unknown_text_vector == [None] or known_text_vectors == [None] or language_labels == [None]:
        return None
    if len(known_text_vectors) != len(language_labels):
        return None

    distances = []
    prediction = []

    for i in known_text_vectors:
        temp = i.copy()
        new_dst = calculate_distance(unknown_text_vector, temp)
        distances.append(new_dst)

    prediction.append(language_labels[0])
    prediction.append(distances[0])

    count = len(distances)
    for j in range(count):
        if distances[j] < prediction[1]:
            prediction[0] = language_labels[j]
            prediction[1] = distances[j]

    return prediction


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
    if unknown_text_vector == [None] or known_text_vector == [None]:
        return None

    distance = 0.0

    count = len(unknown_text_vector)
    for i in range(count):
        temp = unknown_text_vector[i] - known_text_vector[i]
        if temp < 0:
            temp *= (-1)
        distance += temp

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
    # pylint: disable-msg=too-many-locals
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list):
        return None
    if not isinstance(language_labels, list):
        return None
    if unknown_text_vector == [None] or known_text_vectors == [None] or language_labels == [None]:
        return None
    if len(known_text_vectors) != len(language_labels):
        return None

    distances = []
    prediction = []

    for i in known_text_vectors:
        temp = i.copy()
        if metric == 'manhattan':
            new_dst = calculate_distance_manhattan(unknown_text_vector, temp)
            distances.append(new_dst)
        elif metric == 'euclid':
            new_dst = calculate_distance(unknown_text_vector, temp)
            distances.append(new_dst)

    labels_sorted = language_labels.copy()
    temp = dict(zip(labels_sorted, distances))
    labels_sorted.sort(key=temp.get)
    distances.sort()

    klabels = labels_sorted[:k]
    kdists = distances[:k]
    prediction.append(klabels[0])
    prediction.append(kdists[0])

    fqs = get_freq_dict(klabels)

    lbls = list(fqs.keys())
    vals = list(fqs.values())
    if len(set(vals)) < len(vals):
        lbls.sort(key=fqs.get)
        res = lbls[0]
        prediction[0] = res

    return prediction


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
