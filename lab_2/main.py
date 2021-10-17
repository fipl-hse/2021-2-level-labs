"""
Lab 2
Language classification
"""

import math
from lab_1.main import tokenize, remove_stop_words


# 4
def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if not isinstance(tokens, list) or not all(isinstance(i, str) for i in tokens):
        return None
    freq_dict = {}
    for word in tokens:
        if word in freq_dict:
            freq_dict[word] += 1 / len(tokens)
        else:
            freq_dict[word] = 1 / len(tokens)
    for word in freq_dict:
        freq_dict[word] = round(freq_dict[word], 5)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """

    if (not isinstance(texts_corpus, list) or
            not isinstance(language_labels, list) or
            not all(isinstance(i, list) for i in texts_corpus) or
            not all(isinstance(i, str) for i in language_labels)):
        return None
    lang_pr = {}
    for text in range(len(texts_corpus)):
        lang_pr[language_labels[text]] = get_freq_dict(texts_corpus[text])
    return lang_pr


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if (not isinstance(language_profiles, dict) or
            not all(isinstance(key, str) for key in language_profiles.keys()) or
            not all(isinstance(value, dict) for value in language_profiles.values()) or
            not language_profiles.items()):
        return None
    features = []
    for profile in language_profiles.values():
        for word in profile:
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

    if (not isinstance(original_text, list) or
            not isinstance(language_profiles, dict) or
            not all(isinstance(key, str) for key in language_profiles.keys()) or
            not all(isinstance(value, dict) for value in language_profiles.values()) or
            not language_profiles.items()):
        return None
    unique_words = get_language_features(language_profiles)
    text_vector = []
    for word in unique_words:
        freq_list = []
        for lang in language_profiles.values():
            if word in lang:
                freq_list.append(lang.get(word) if word in original_text else 0)
        text_vector.append(sorted(freq_list)[0])
    return text_vector


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """

    if (not isinstance(unknown_text_vector, list) or
            not isinstance(known_text_vector, list) or
            not all(isinstance(i, (float, int)) for i in unknown_text_vector) or
            not all(isinstance(i, (float, int)) for i in known_text_vector)):
        return None
    sq_dif = []
    for index, vector in enumerate(unknown_text_vector):
        sq_dif.append((vector - known_text_vector[index]) ** 2)
    return round(math.sqrt(sum(sq_dif)), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """

    if (not isinstance(unknown_text_vector, list) or
            not isinstance(known_text_vectors, list) or
            not isinstance(language_labels, list)):
        return None
    if (not all(isinstance(i, (float, int)) for i in unknown_text_vector) or
            not all(isinstance(i, list) for i in known_text_vectors) or
            not all(isinstance(i, str) for i in language_labels)):
        return None
    if len(known_text_vectors) != len(language_labels):
        return None
    all_dist = []
    for vector in known_text_vectors:
        all_dist.append(calculate_distance(unknown_text_vector, vector))
    dist = sorted(all_dist)[0]
    lang = language_labels[all_dist.index(dist)]
    return [lang, dist]


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """

    if (not isinstance(unknown_text_vector, list) or
            not isinstance(known_text_vector, list) or
            not all(isinstance(i, (float, int)) for i in unknown_text_vector) or
            not all(isinstance(i, (float, int)) for i in known_text_vector)):
        return None
    man_dif = []
    for index, vector in enumerate(unknown_text_vector):
        man_dif.append(abs(vector - known_text_vector[index]))
    return round(sum(man_dif), 5)


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

    if (not isinstance(unknown_text_vector, list) or
            not isinstance(known_text_vectors, list) or
            not isinstance(language_labels, list)):
        return None
    if (not all(isinstance(i, (float, int)) for i in unknown_text_vector) or
            not all(isinstance(i, list) for i in known_text_vectors) or
            not all(isinstance(i, str) for i in language_labels)):
        return None
    if (len(known_text_vectors) != len(language_labels) or
            not isinstance(k, int) or metric not in ('euclid', 'manhattan')):
        return None
    dist_list = []
    for lang in known_text_vectors:
        if metric == 'euclid':
            dist_list.append(calculate_distance(unknown_text_vector, lang))
        elif metric == 'manhattan':
            dist_list.append(calculate_distance_manhattan(unknown_text_vector, lang))
    close_dist = sorted(dist_list)[:k]
    close_lang = [language_labels[dist_list.index(dist)] for dist in close_dist]
    count_lang = dict((lang, close_lang.count(lang)) for lang in set(close_lang))
    if list(count_lang.values())[0] == list(count_lang.values())[1]:
        closest_lang = close_lang[0]
    else:
        closest_lang = sorted(count_lang, key=count_lang.get, reverse=True)[0]
    return [closest_lang, close_dist[0]]


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if (not isinstance(original_text, list) or
            not isinstance(language_profiles, dict) or
            not all(isinstance(key, str) for key in language_profiles.keys()) or
            not all(isinstance(value, dict) for value in language_profiles.values()) or
            not language_profiles.items()):
        return None
    unique_words = get_language_features(language_profiles)
    word_scores = []
    for index, word in enumerate(unique_words):
        for lang in language_profiles.values():
            if word in lang:
                word_scores.append([index, lang.get(word)])
    sparse_vector = [word_scores[index] for index, word in enumerate(unique_words) if word in original_text]
    return sparse_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """

    if (not isinstance(unknown_text_vector, list) or
            not isinstance(known_text_vector, list) or
            not all(isinstance(i, list) for i in unknown_text_vector) or
            not all(isinstance(i, list) for i in known_text_vector)):
        return None
    unknown_dict = dict(unknown_text_vector)
    known_dict = dict(known_text_vector)
    combine_dict = dict(unknown_text_vector[:])
    combine_dict.update(known_dict)
    for index in combine_dict:
        if index in unknown_dict and index in known_dict:
            combine_dict[index] = unknown_dict[index] - known_dict[index]
    distance = math.sqrt(sum(score**2 for score in combine_dict.values()))
    return round(distance, 5)


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

    if (not isinstance(unknown_text_vector, list) or
            not isinstance(known_text_vectors, list) or
            not isinstance(language_labels, list)):
        return None
    if (not all(isinstance(i, list) for i in unknown_text_vector) or
            not all(isinstance(i, list) for i in known_text_vectors) or
            not all(isinstance(i, str) for i in language_labels)):
        return None
    if (len(known_text_vectors) != len(language_labels) or
            not isinstance(k, int)):
        return None
    dist_list = []
    for vector in known_text_vectors:
        dist_list.append(calculate_distance_sparse(unknown_text_vector, vector))
    close_dist = sorted(dist_list)[:k]
    close_lang = [language_labels[dist_list.index(dist)] for dist in close_dist]
    count_lang = dict((lang, close_lang.count(lang)) for lang in set(close_lang))
    if list(count_lang.values())[0] == list(count_lang.values())[1]:
        closest_lang = close_lang[0]
    else:
        closest_lang = sorted(count_lang, key=count_lang.get, reverse=True)[0]
    return [closest_lang, close_dist[0]]
