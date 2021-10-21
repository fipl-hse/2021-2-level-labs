"""
Lab 2
Language classification
"""

from math import sqrt, fabs
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
    if len(tokens) > 0 and not isinstance(tokens[0], str):
        return None
    set_words = set(tokens.copy())
    number_of_tokens = len(tokens)
    freq_dict = {}
    for word in set_words:
        freq_of_tokens = tokens.count(word)
        freq_dict.update({word: round(freq_of_tokens / number_of_tokens, 5)})
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
    if not isinstance(texts_corpus[0], list):
        return None
    language_profiles = {language_labels[0]: get_freq_dict(texts_corpus[0])}
    language_profiles.update({language_labels[-1]: get_freq_dict(texts_corpus[-1])})
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    lst_of_tokens = []
    for lang in language_profiles:
        for key in language_profiles[lang]:
            lst_of_tokens.append(key)
    if len(lst_of_tokens) == 0:
        return None
    lst_of_tokens = sorted(lst_of_tokens)
    return lst_of_tokens


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) or not isinstance(language_profiles, dict):
        return None
    vectors = []
    uni_tokens = get_language_features(language_profiles)
    for word in uni_tokens:
        if word in original_text:
            for lang in language_profiles:
                for key in language_profiles[lang]:
                    if key == word:
                        vectors.append(language_profiles[lang][key])
        else:
            vectors.append(0)
    return vectors


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list):
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    if all(isinstance(i, (int, float)) for i in unknown_text_vector) \
            and all(isinstance(e, (int, float)) for e in known_text_vector):
        distance = sqrt(sum((j - k) ** 2 for j, k
                            in zip(unknown_text_vector, known_text_vector)))
        distance = round(distance, 5)
        return distance
    return None


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list):
        return None
    if len(language_labels) < 3:
        return None
    score_list = []
    for i in known_text_vectors:
        score = calculate_distance(unknown_text_vector, i)
        score_list.append(score)
    label_and_score = dict(zip(language_labels, score_list))
    min_value = min(label_and_score.values())
    language_score = []
    for k in label_and_score:
        if label_and_score[k] == min_value:
            language_score.append(k)
    language_score.append(min_value)
    return language_score


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list):
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    if all(isinstance(i, (int, float)) for i in unknown_text_vector) \
            and all(isinstance(e, (int, float)) for e in known_text_vector):
        manhattan_distance = sum(fabs(j - k) for j, k
                                 in zip(unknown_text_vector, known_text_vector))
        manhattan_distance = round(manhattan_distance, 5)
        return manhattan_distance
    return None


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
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not isinstance(k, int) \
            or not isinstance(metric, str):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    score_list = []
    if metric == 'manhattan':
        for i in known_text_vectors:
            score_list.append(calculate_distance_manhattan(unknown_text_vector, i))
    elif metric == 'euclid':
        for i in known_text_vectors:
            score_list.append(calculate_distance(unknown_text_vector, i))
    else:
        return None
    knn_score = sorted(score_list)[:k]
    closest_lang = []
    for i in knn_score:
        position = score_list.index(i)
        label = language_labels[position]
        closest_lang.append(label)
    predict_label = {}
    for lang in closest_lang:
        if lang not in predict_label:
            predict_label[lang] = 1
        else:
            predict_label[lang] += 1
    predict_lang = max(predict_label, key=predict_label.get)
    prediction = [predict_lang, min(score_list)]
    return prediction


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
    text_vector_sparse = []
    uni_tokens = get_language_features(language_profiles)
    for word in uni_tokens:
        if word in original_text:
            for lang in language_profiles:
                for key in language_profiles[lang]:
                    if key == word:
                        mini_list = [uni_tokens.index(word), language_profiles[lang][key]]
                        text_vector_sparse.append(mini_list)
        else:
            continue
    return text_vector_sparse


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    if all(isinstance(i, list) for i in unknown_text_vector) \
            and all(isinstance(e, list) for e in known_text_vector):
        dict_unknown_text_vector = dict(unknown_text_vector)
        for elem in known_text_vector:
            if elem[0] in dict_unknown_text_vector.keys():
                dict_unknown_text_vector[elem[0]] -= elem[1]
            else:
                dict_unknown_text_vector[elem[0]] = elem[1]
        distance = sqrt(sum(elem ** 2 for elem in dict_unknown_text_vector.values()))
        distance = round(distance, 5)
        return distance
    return None


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
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not isinstance(k, int):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    sparse_score_list = []
    for i in known_text_vectors:
        sparse_score_list.append(calculate_distance_sparse(unknown_text_vector, i))
    knn_sparse_score = sorted(sparse_score_list)[:k]
    closest_lang = []
    for i in knn_sparse_score:
        position = sparse_score_list.index(i)
        label = language_labels[position]
        closest_lang.append(label)
    predict_label = {}
    for lang in closest_lang:
        if lang not in predict_label:
            predict_label[lang] = 1
        else:
            predict_label[lang] += 1
    predict_lang = max(predict_label, key=predict_label.get)
    prediction = [predict_lang, min(sparse_score_list)]
    return prediction
