"""
Lab 2
Language classification
"""


from lab_1.main import tokenize
from lab_1.main import remove_stop_words
from math import sqrt

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
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token in freq_dict:
            freq_dict[token] += 1 / len(tokens)
        else:
            freq_dict[token] = 1 / len(tokens)
    for k, v in freq_dict.items():
        v = round(v, 5)
        freq_dict[k] = v
    return freq_dict
    pass

def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not isinstance(texts_corpus, list):
        return None
    if not isinstance(language_labels, list):
        return None
    language_profiles = {}
    lang_freq_dict = []
    for i in texts_corpus:
        if not isinstance(i, list):
            return None
        lang_freq_dict.append(get_freq_dict(i))
    for label in range(len(language_labels)):
        language_profiles[language_labels[label]] = lang_freq_dict[label]
    return language_profiles
    pass

def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    unique_words = []
    for k, v in language_profiles.items():
        for k in language_profiles[k].keys():
            unique_words.append(k)
    unique_words.sort(key=str.lower)
    for i in unique_words:
        if not isinstance(i, str):
            return None
        return unique_words
    pass

def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list):
        return None
    if not isinstance(language_profiles, dict):
        return None
    unique_words = get_language_features(language_profiles)
    text_vector = []
    for word in unique_words:
        if word not in original_text:
            text_vector.append(0)
        elif word in original_text:
            for profile in language_profiles.values():
                for k in profile.keys():
                    if k == word:
                        value = profile.get(word)
                        text_vector.append(value)
    return text_vector
    pass

# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list):
        return None
    if not isinstance(known_text_vector, list):
        return None
    dist = 0
    for i in range(len(unknown_text_vector)):
        for d in unknown_text_vector:
            if not isinstance(d, (int, float)):
                return None
        for d in known_text_vector:
            if not isinstance(d, (int, float)):
                return None
        dist += (unknown_text_vector[i] - known_text_vector[i]) ** 2
    return round(sqrt(dist), 5)
    pass

def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list):
        return None
    if not isinstance(known_text_vectors, list):
        return None
    if not isinstance(language_labels, list):
        return None
    lang_score = []
    dist_lst = []
    for i in known_text_vectors:
        dist = calculate_distance(unknown_text_vector, i)
        dist_lst.append(dist)
    min_dist = dist_lst.index(min(dist_lst))
    for i in range(len(language_labels)):
        predict_label = language_labels[min_dist]
    lang_score.append(predict_label)
    lang_score.append(min(dist_lst))
    if len(known_text_vectors) != len(language_labels):
        return None
    for element in lang_score:
        if not isinstance(element, str):
            return None
        return lang_score
    pass

# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list):
        return None
    if not isinstance(known_text_vector, list):
        return None
    dist = 0
    for i in range(len(unknown_text_vector)):
        for d in unknown_text_vector:
            if not isinstance(d, (int, float)):
                return None
        for d in known_text_vector:
            if not isinstance(d, (int, float)):
                return None
        dist += abs(unknown_text_vector[i] - known_text_vector[i])
    return dist
    pass

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
    if not isinstance(unknown_text_vector, list):
        return None
    if not isinstance(known_text_vectors, list):
        return None
    if not isinstance(language_labels, list):
        return None
    if not isinstance(k, int):
        return None
    if not isinstance(metric, str):
        return None
    lst = []
    for i in known_text_vectors:
        if metric == 'manhattan':
            dist = calculate_distance_manhattan(unknown_text_vector, i)
            lst.append(dist)
        elif metric == 'euclid':
            dist = calculate_distance(unknown_text_vector, i)
            lst.append(dist)
    k_lst = sorted(lst)
    kn_lst = k_lst[:(k+1)]
    labels = []
    for i in kn_lst:
        ind = lst.index(i)
        if len(language_labels) != len(known_text_vectors):
            return None
        else:
            label = language_labels[ind]
            labels.append(label)
        labels_dict = {}
        for label in labels:
            if not isinstance(label, str):
                return None
            if label in labels_dict:
                labels_dict[label] += 1
            else:
                labels_dict[label] = 1
    predict_label = max(labels_dict, key=labels_dict.get)
    predict_result = [predict_label, round(min(lst), 5)]
    return predict_result
    pass


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
    if not isinstance(language_profiles, dict):
        return None
    unique_words = get_language_features(language_profiles)
    text_vector = []
    for i in unique_words:
        if i in original_text:
            for profile in language_profiles.values():
                for k in profile.keys():
                    if k == i:
                        value = profile.get(i)
                        text_vector.append([unique_words.index(i), value])
    return text_vector
    pass


#def calculate_distance_sparse(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """



#def predict_language_knn_sparse(unknown_text_vector: list, known_text_vectors: list, language_labels: list, k=1) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
        using knn based algorithm
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vectors: a list of sparse vectors for known texts
    :param language_labels: language labels for each known text
    :param k: the number of neighbors to choose label from
    """
