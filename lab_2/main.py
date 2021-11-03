"""
Lab 2
Language classification
"""

from math import sqrt
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
    length = len(tokens)
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    for token in freq_dict:
        freq_dict[token] = round(freq_dict[token]/length, 5)
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
    for label, text in zip(language_labels, texts_corpus):
        if not isinstance(label, str) or not isinstance(text, list):
            return None
        language_profiles[label] = get_freq_dict(text)
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
    for freq_dict in language_profiles.values():
        if not isinstance(freq_dict, dict):
            return None
        for word in freq_dict.keys():
            if not isinstance(word, str):
                return None
            features.append(word)
    features = sorted(features)
    return features


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
    features = get_language_features(language_profiles)
    for word in features:
        if word in original_text:
            for freq_dict in language_profiles.values():
                for key, value in freq_dict.items():
                    if key == word:
                        text_vector.append(value)
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
    distance = 0
    for unknown_vector, known_vector in zip(unknown_text_vector, known_text_vector):
        if not isinstance(unknown_vector, (int, float))\
                or not isinstance(known_vector, (int, float)):
            return None
        distance += (unknown_vector - known_vector) ** 2
    return round(sqrt(distance), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not len(language_labels) == len(known_text_vectors):
        return None
    labels_distances = []
    for language_label, known_text_vector in zip(language_labels, known_text_vectors):
        if not isinstance(known_text_vector, list) or not isinstance(unknown_text_vector, list) \
                or not isinstance(language_label, str):
            return None
        distance = calculate_distance(unknown_text_vector, known_text_vector)
        labels_distances.append(tuple((language_label, distance)))
    sorted_labels_distances = sorted(labels_distances, key=lambda x: x[1])
    prediction = list(sorted_labels_distances[0])
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
    distance = 0
    for unknown_vector, known_vector in zip(unknown_text_vector, known_text_vector):
        if not isinstance(unknown_vector, (int, float))\
                or not isinstance(unknown_vector, (int, float)):
            return None
        distance += abs(unknown_vector - known_vector)
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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not isinstance(k, int) or not isinstance(metric, str):
        return None
    if not len(language_labels) == len(known_text_vectors):
        return None
    labels_distances = []
    for language_label, known_text_vector in zip(language_labels, known_text_vectors):
        if not isinstance(known_text_vector, list) or not isinstance(unknown_text_vector, list) \
                or not isinstance(language_label, str):
            return None
        if metric == 'manhattan':
            distance = calculate_distance_manhattan(unknown_text_vector, known_text_vector)
            labels_distances.append(tuple((language_label, distance)))
        elif metric == 'euclid':
            distance = calculate_distance(unknown_text_vector, known_text_vector)
            labels_distances.append(tuple((language_label, distance)))
    sorted_labels_distances = sorted(labels_distances, key=lambda x: x[1])[:k]
    labels_frequency = {}
    for label, distance in sorted_labels_distances:
        if label not in labels_frequency:
            labels_frequency[label] = 1
        else:
            labels_frequency[label] += 1
    prediction = [max(labels_frequency, key=labels_frequency.get), sorted_labels_distances[0][1]]
    return prediction


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
            and all(isinstance(i, str) for i in original_text)
            and isinstance(language_profiles, dict)
            and language_profiles
    ):
        return None

    features = get_language_features(language_profiles)
    sparse_vector = []

    vector = dict.fromkeys(features, 0)
    for language_profile in language_profiles.values():
        for word, freq in language_profile.items():
            vector[word] = freq
    for index, feature in enumerate(features):
        if feature in original_text:
            sparse_vector.append([index, vector[feature]])
    return sparse_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not (
            isinstance(unknown_text_vector, list)
            and isinstance(known_text_vector, list)
            and all(isinstance(i, list) for i in unknown_text_vector)
            and all(isinstance(i, list) for i in known_text_vector)
    ):
        return None

    unknown_text_dict = dict(unknown_text_vector)
    known_text_dict = dict(known_text_vector)
    mixed_dict = {**unknown_text_dict, **known_text_dict}

    for key, value in unknown_text_dict.items():
        if key in known_text_dict:
            mixed_dict[key] = value - known_text_dict[key]
    euclidean_distance = 0
    for value in mixed_dict.values():
        euclidean_distance += value ** 2
    return round(sqrt(euclidean_distance), 5)


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
            and isinstance(known_text_vectors, list)
            and all(isinstance(i, list) for i in unknown_text_vector)
            and all(isinstance(i, list) for i in known_text_vectors)
            and isinstance(language_labels, list)
            and all(isinstance(i, str) for i in language_labels)
            and len(known_text_vectors) == len(language_labels)
            and isinstance(k, int)
    ):
        return None

    distances = []
    for i in known_text_vectors:
        distances.append(calculate_distance_sparse(unknown_text_vector, i))

    knn_distances_sparse = sorted(distances)[:k]
    closest_languages = []
    for i in knn_distances_sparse:
        ind = distances.index(i)
        label = language_labels[ind]
        closest_languages.append(label)

    predict_label = {}
    for language in closest_languages:
        if language not in predict_label:
            predict_label[language] = 1
        else:
            predict_label[language] += 1
    predict_language = max(predict_label, key=predict_label.get)
    prediction = [predict_language, min(distances)]
    return prediction
