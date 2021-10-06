"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words


def elements_instances(iterable, *types):
    """
    Checks if all elements in an iterable are instances of allowed types
    :param iterable: an iterable with elements to be checked
    :params types: types allowed to be in the iterable
    """
    return all(any(isinstance(elem, t) for t in types) for elem in iterable)

# 4
def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    if not elements_instances(tokens, str):
        return None
    freq_dict = {}
    for token in tokens:
        if token not in freq_dict:
            freq_dict[token] = 0
        freq_dict[token] += 1 / len(tokens)
    return {k: round(v, 5) for k, v in freq_dict.items()}


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if (not isinstance(texts_corpus, list)
            or not isinstance(language_labels, list)):
        return None
    if (not elements_instances(texts_corpus, list)
            or not elements_instances(language_labels, str)):
        return None
    return {k: get_freq_dict(v) for k, v in zip(language_labels, texts_corpus)}


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    texts = [freq_dict.keys() for freq_dict in language_profiles.values()]
    if not texts:
        return None
    return sorted(set().union(*texts))


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list):
        return None
    if not elements_instances(original_text, str):
        return None
    features = get_language_features(language_profiles)
    if not features:
        return None
    original_text = set(original_text)
    max_scores = {word: 0 for word in features}
    for profile in language_profiles.values():
        for word, score in profile.items():
            if score > max_scores[word] and word in original_text:
                max_scores[word] = score
    return [max_scores[word] for word in features]


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vector, list)):
        return None
    if not elements_instances(unknown_text_vector + known_text_vector, int, float):
        return None
    distance = sum((a-b)**2 for a, b in zip(unknown_text_vector, known_text_vector))**0.5
    return round(float(distance), 5)


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
            or not isinstance(language_labels, list)):
        return None
    if (not elements_instances(unknown_text_vector, int, float)
            or not elements_instances(known_text_vectors, list)
            or not elements_instances(language_labels, str)):
        return None
    if len(known_text_vectors) != len(language_labels):
        return None
    scores = [calculate_distance(unknown_text_vector, vector) for vector in known_text_vectors]
    return list(min(zip(language_labels, scores), key=lambda x: x[1]))


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
    if not elements_instances(unknown_text_vector + known_text_vector, int, float):
        return None
    distance = sum(abs(a-b) for a, b in zip(unknown_text_vector, known_text_vector))
    return round(float(distance), 5)


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
    if (not elements_instances(unknown_text_vector, int, float)
            or not elements_instances(known_text_vectors, list)
            or not elements_instances(language_labels, str)):
        return None
    if len(known_text_vectors) != len(language_labels):
        return None
    distance = calculate_distance_manhattan if metric == "manhattan" else calculate_distance
    scores = [distance(unknown_text_vector, vector) for vector in known_text_vectors]
    best_fits = sorted(zip(language_labels, scores), key=lambda x: x[1])[:k]

    label_freq = {}
    for label, _ in best_fits:
        if label not in label_freq:
            label_freq[label] = 0
        label_freq[label] += 1
    return [max(label_freq, key=label_freq.get), min(scores)]


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list):
        return None
    if not elements_instances(original_text, str):
        return None
    features = get_language_features(language_profiles)
    if not features:
        return None

    original_text = set(original_text)
    max_scores = {word: 0 for word in features}
    for profile in language_profiles.values():
        for word, score in profile.items():
            if score > max_scores[word] and word in original_text:
                max_scores[word] = score

    return [[i, max_scores[word]] for i, word in enumerate(features) if word in original_text]


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
