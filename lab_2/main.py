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
    pass
    if not isinstance(tokens, list):
        return None
    frequency_dictionary = {}
    for word in tokens:
        if isinstance(word, str):
            if word in frequency_dictionary:
                frequency_dictionary[word] += 1
            else:
                frequency_dictionary[word] = 1
        else:
            return None
    for key, value in frequency_dictionary.items():
        frequency_dictionary[key] = round((value / len(tokens)),5)
    return frequency_dictionary

def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    pass
    language_profiles = {}
    if (not isinstance(texts_corpus, list)) or (not isinstance(language_labels, list)):
        return None
    for corpus, label in zip(texts_corpus,language_labels):
        if isinstance(corpus, str) or isinstance(label, str):
            language_profiles[label] = get_freq_dict(corpus)
        else:
            return None
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    pass
    features = []
    if (not isinstance(language_profiles,dict)) or (language_profiles == {}):
        return None
    for tokens_and_frequencies in language_profiles.values():
        for token in tokens_and_frequencies:
            features.append(token)
            features = sorted(features)
    return features


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    pass
    if (not isinstance(original_text,list)) or (not isinstance(language_profiles,dict)):
        return None
    features = get_language_features(language_profiles)
    vector = dict.fromkeys(features,0)
    for profile in language_profiles.values():
        for unique_word, value_score in profile.items():
            if (value_score > vector[unique_word]) and (unique_word in original_text):
                vector[unique_word] = value_score
    new_vector = list(vector.values())
    return new_vector

# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    pass
    if not isinstance(unknown_text_vector,list) or not isinstance(known_text_vector,list):
        return None
    for el_unknown_vector in unknown_text_vector:
        if not isinstance(el_unknown_vector, (float, int)):
            return None
    for el_known_vector in known_text_vector:
        if not isinstance(el_known_vector, (float, int)):
            return None
    distance = 0
    for i, el in enumerate(unknown_text_vector):
        distance += ((unknown_text_vector[i] - known_text_vector[i]) ** 2)
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
    pass

    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or len(language_labels) != len(known_text_vectors):
        return None
    all_distance = []
    for vectors in known_text_vectors:
        if not isinstance(vectors, list):
            return None
        distance = calculate_distance(unknown_text_vector, vectors)
        all_distance.append(distance)
    min_distance = min(all_distance)
    language_score = [language_labels[all_distance.index(min_distance)], min_distance]
    return language_score



# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    pass
    if not isinstance(unknown_text_vector,list) or not isinstance(known_text_vector,list):
        return None
    for el_unknown_vector in unknown_text_vector:
        if not isinstance(el_unknown_vector, (float, int)):
            return None
    for el_known_vector in known_text_vector:
        if not isinstance(el_known_vector, (float, int)):
            return None
    distance = 0
    for i, el in enumerate(unknown_text_vector):
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
    pass
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not isinstance(k, int) \
            or not isinstance(metric, str) \
            or len(language_labels) != len(known_text_vectors):
        return None
    if metric == "manhattan":
        distances = [calculate_distance_manhattan(unknown_text_vector, vectors)
                     for vectors in known_text_vectors]
    elif metric == 'euclid':
        distances = [calculate_distance(unknown_text_vector, vectors)
                     for vectors in known_text_vectors]
    sorted_distance = sorted(distances)[:k]
    languages = [language_labels[distances.index(distance)] for distance in sorted_distance]
    list_of_tuple = [tpl for tpl in zip(languages, sorted_distance)]
    list_of_tuples = sorted(list_of_tuple, key=lambda i: i[1])
    dict_of_tuples_and_counts = {}
    for language, dist in list_of_tuples:
        if language in dict_of_tuples_and_counts.keys():
            dict_of_tuples_and_counts[language] += 1
        else:
            dict_of_tuples_and_counts[language] = 1
    most_frequent_language = max(dict_of_tuples_and_counts, key=dict_of_tuples_and_counts.get)
    list_with_language_and_min_distance = [most_frequent_language, float(min(sorted_distance))]
    return list_with_language_and_min_distance


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    pass
    if not isinstance(original_text,list) or not isinstance(language_profiles,dict):
        return None
    for word in original_text:
        if not isinstance(word, str):
            return None
    list_with_word_and_score = []
    new_list_with_word_and_score = []
    features = get_language_features(language_profiles)
    vector = dict.fromkeys(features, 0)
    for profile in language_profiles.values():
        for unique_word, value_score in profile.items():
            if (value_score > vector[unique_word]) and (unique_word in original_text):
                vector[unique_word] = value_score
    for key_word, score in vector.items():
        list_with_word_and_score.append([key_word, score])
        for index, lst in enumerate(list_with_word_and_score):
            if lst[1] == 0:
                list_with_word_and_score.pop(index)
    for new_lst in list_with_word_and_score:
        new_list_with_word_and_score.append([features.index(new_lst[0]), new_lst[1]])
    return new_list_with_word_and_score



def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    pass
    if not isinstance(unknown_text_vector,list) or not isinstance(known_text_vector,list):
        return None
    for vector in unknown_text_vector:
        if not isinstance(vector, list):
            return None
    for vector in known_text_vector:
        if not isinstance(vector, list):
            return None
    distance = 0
    dictionary_of_indices_and_scores = dict(unknown_text_vector)
    for index_and_score in known_text_vector:
        if index_and_score[0] not in dictionary_of_indices_and_scores:
            dictionary_of_indices_and_scores[index_and_score[0]] = index_and_score[1]
        else:
            dictionary_of_indices_and_scores[index_and_score[0]] -= index_and_score[1]
    for value in dictionary_of_indices_and_scores.values():
        distance += value ** 2
    return round(distance ** 0.5, 5)

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
    if not isinstance(unknown_text_vector,list) or not isinstance(known_text_vectors,list) \
            or not isinstance(language_labels,list) or not isinstance(k,int):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    distances = [calculate_distance_sparse(unknown_text_vector,vector)
                 for vector in known_text_vectors]
    sorted_distance = sorted(distances)[:k]
    languages = [language_labels[distances.index(distance)] for distance in sorted_distance]
    list_of_tuple = [tpl for tpl in zip(languages, sorted_distance)]
    list_of_tuples = sorted(list_of_tuple, key=lambda i: i[1])
    dict_of_tuples_and_counts = {}
    for language, dist in list_of_tuples:
        if language in dict_of_tuples_and_counts.keys():
            dict_of_tuples_and_counts[language] += 1
        else:
            dict_of_tuples_and_counts[language] = 1
    most_frequent_language = max(dict_of_tuples_and_counts, key=dict_of_tuples_and_counts.get)
    list_with_language_and_min_distance = [most_frequent_language, float(min(sorted_distance))]
    return list_with_language_and_min_distance
