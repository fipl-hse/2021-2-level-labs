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
    if (not isinstance(tokens, list)) or tokens == [None]:
        return None
    word_counter = len(tokens)
    counted_words_dict = {}
    for token in tokens:
        if token not in counted_words_dict.keys():
            counted_words_dict[token] = 1
        else:
            counted_words_dict[token] += 1
    for key, value in counted_words_dict.items():
        counted_words_dict[key] = round(value / word_counter, 5)
    return counted_words_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(texts_corpus, list) and isinstance(language_labels, list)):
        return None
    language_profiles = {}
    freq_lists = []
    for text in texts_corpus:
        freq_lists.append(get_freq_dict(text))
        if text is None:
            return None
    for i, label in enumerate(language_labels):
        if label not in language_profiles.keys():
            language_profiles[label] = freq_lists[i]
        else:
            language_profiles[label].update(freq_lists[i])
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(language_profiles, dict) and len(language_profiles) != 0):
        return None
    features = []
    for value in language_profiles.values():
        features.extend(value.keys())
    features.sort()
    return features


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(original_text, list) and isinstance(language_profiles, dict)):
        return None
    vector = []
    for word in get_language_features(language_profiles):
        if word in original_text:
            for language in language_profiles:
                if word in language_profiles[language]:
                    vector.append(language_profiles[language][word])
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
    future_result = 0
    for i, coordinate in enumerate(unknown_text_vector):
        if not isinstance(coordinate, (float, int)):
            return None
        future_result += (coordinate - known_text_vector[i]) ** 2
    result = round(future_result ** 0.5, 5)
    return result


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:  ##not float?
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vectors, list) and
            isinstance(language_labels, list)) or len(known_text_vectors) != len(language_labels):
        return None
    vectors_results = []
    for vector in known_text_vectors:
        result_vect = calculate_distance(unknown_text_vector, vector)
        if result_vect is None:
            return None
        vectors_results.append(result_vect)
    min_score = min(vectors_results)
    predicted_and_score = [language_labels[vectors_results.index(min_score)], round(min_score, 5)]
    return predicted_and_score


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vector, list)):
        return None
    future_result = 0
    for i, coordinate in enumerate(unknown_text_vector):
        if not isinstance(coordinate, (float, int)):
            return None
        future_result += abs(coordinate - known_text_vector[i])
    return round(future_result, 5)


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
    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vectors, list)
            and isinstance(language_labels, list) and isinstance(k, int)
            and isinstance(metric, str)) or len(language_labels) != len(known_text_vectors):
        return None
    results_list = []
    top_languages = {}
    max_quantity = 0
    predicted_l = ''
    absolute_minimum = 100
    re_lang = ()
    for i, vector in enumerate(known_text_vectors):
        if metric == 'manhattan':
            re_lang = (calculate_distance_manhattan(unknown_text_vector, vector),
                       language_labels[i])
        elif metric == 'euclid':
            re_lang = (calculate_distance(unknown_text_vector, vector), language_labels[i])
        if (re_lang[0] is None) or not isinstance(re_lang[1], str):
            return None
        results_list.append(re_lang)
    results_list.sort()
    for i in range(k):
        if results_list[i][1] not in top_languages.keys():
            top_languages[results_list[i][1]] = [results_list[i][0]]
        else:
            top_languages[results_list[i][1]].append(results_list[i][0])
    for language, vectors in top_languages.items():
        if len(vectors) > max_quantity:
            predicted_l = language
            max_quantity = len(vectors)
            absolute_minimum = min(absolute_minimum,min(vectors))
        elif len(vectors) == max_quantity:
            if min(vectors) < min(top_languages[predicted_l]):
                predicted_l = language
    return [predicted_l, absolute_minimum]


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
