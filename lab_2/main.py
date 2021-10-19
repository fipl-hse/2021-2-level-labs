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
    if not isinstance(tokens, list):
        return None
    freq_dict = {}
    frequency = {}
    for token in tokens:
        if isinstance(token, str):
            if token in freq_dict:
                freq_dict[token] += 1
            else:
                freq_dict[token] = 1
            frequency[token] = round(freq_dict[token]/len(tokens),5)
        else:
            return None
    return frequency



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
    for label in language_labels:
        if not isinstance(label, str):
            return None
    for text in texts_corpus:
        if not isinstance(text, list):
            return None
    language_profile = {}
    for index, _ in enumerate(language_labels):
        language_profile [language_labels[index]] = get_freq_dict(texts_corpus[index])
    return language_profile



def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict) or not language_profiles:
        return None
    unique_tokens = []
    for value in language_profiles.values():
        for value_1 in value:
            if value_1 not in unique_tokens:
                unique_tokens.append(value_1)
    unique_tokens.sort()
    return unique_tokens



def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance (original_text, list) or not isinstance(language_profiles,dict):
        return None
    for word in original_text:
        if not isinstance(word, str):
            return None
    text_vector = []
    unique_tokens = get_language_features(language_profiles)
    max_unique_token_freq = {}
    for token in unique_tokens:
        token_freq_value = 0
        for language_profile in language_profiles.keys():
            if language_profiles[language_profile].get(token, 0)>token_freq_value:
                token_freq_value = language_profiles[language_profile].get(token, 0)
        max_unique_token_freq [token] = token_freq_value
    for token_1 in unique_tokens:
        if token_1 in original_text:
            text_vector.append(max_unique_token_freq[token_1])
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
    if not isinstance (unknown_text_vector, list) or not isinstance (known_text_vector, list):
        return None
    for unknown_vector in unknown_text_vector:
        if not isinstance (unknown_vector, (float, int)):
            return None
    for known_vector in known_text_vector:
        if not isinstance (known_vector, (float, int)):
            return None
    distance = 0
    for index, _ in enumerate(unknown_text_vector):
        distance += ((unknown_text_vector [index] - known_text_vector [index])**2)
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
    if not isinstance (unknown_text_vector,list) \
            or not isinstance (known_text_vectors, list) \
            or not isinstance (language_labels, list):
        return None
    for vector in known_text_vectors:
        if not isinstance(vector, list):
            return None
    if len(language_labels) != len(known_text_vectors):
        return None
    result = []
    distances = []
    for vector in known_text_vectors:
        distance = calculate_distance(unknown_text_vector, vector)
        distances.append(distance)
    predict_language_distance = min(distances)
    for index, value in enumerate(distances):
        if not isinstance(value, (int,float)):
            return None
        if value == predict_language_distance:
            result = [language_labels[index], value]

    return result


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) \
            or not isinstance (known_text_vector, list):
        return None
    for unknown_vector in unknown_text_vector:
        if not isinstance (unknown_vector, (float,int)):
            return None
    for known_vector in known_text_vector:
        if not isinstance(known_vector, (float,int)):
            return None
    distance = 0
    for index, _ in enumerate (unknown_text_vector):
        distance += (abs(unknown_text_vector[index] - known_text_vector[index]))
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
    if not isinstance (unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not isinstance(k, int) or not isinstance (metric, str):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    calculate_distances = []
    if metric == "manhattan":
        for vector in known_text_vectors:
            calculate_distances.append(calculate_distance_manhattan(unknown_text_vector, vector))
    elif metric == "euclid":
        for vector in known_text_vectors:
            calculate_distances.append(calculate_distance(unknown_text_vector, vector))
    distances = sorted(calculate_distances)[:k]
    sorted_languages = []
    for distance in distances:
        sorted_languages.append(language_labels[calculate_distances.index(distance)])
    list_of_label_and_distances = list(zip(sorted_languages, distances))
    list_of_label_and_distances = sorted(list_of_label_and_distances, key=lambda i: i[1])
    dict_of_label_and_distances = {}
    for pair in list_of_label_and_distances:
        if pair[0] in dict_of_label_and_distances.keys():
            dict_of_label_and_distances[pair[0]] += 1
        else:
            dict_of_label_and_distances[pair[0]] = 1
    common_languages = max(dict_of_label_and_distances, key= dict_of_label_and_distances.get)
    result = [common_languages, round(float(min(distances)),5)]
    return result



# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance (original_text, list) or not isinstance(language_profiles,dict):
        return None
    for word in original_text:
        if not isinstance(word, str):
            return None
    sparse_vector = []
    unique_tokens = get_language_features(language_profiles)
    dict_values_vectors = {}
    for language_profile in language_profiles.values():
        for index, token in language_profile.items():
            if token > dict_values_vectors.get(index, 0):
                dict_values_vectors[index] = token
    for index, unique_token in enumerate(unique_tokens):
        if unique_token in original_text:
            sparse_vector.append([index, dict_values_vectors[unique_token]])
    return sparse_vector


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    if not isinstance (unknown_text_vector, list) or not isinstance (known_text_vector, list):
        return None
    for unknown_vector in unknown_text_vector:
        if not isinstance (unknown_vector, list):
            return None
    for known_vector in known_text_vector:
        if not isinstance (known_vector, list):
            return None
    distance = 0
    dictionary_of_vectors = dict(unknown_text_vector)
    for _, value in enumerate(known_text_vector):
        if value[0] not in dictionary_of_vectors:
            dictionary_of_vectors[value[0]] = value[1]
        else:
            dictionary_of_vectors[value[0]] = dictionary_of_vectors[value[0]] - value[1]
    list_of_vectors = list(dictionary_of_vectors.values())
    for value in list_of_vectors:
        distance += value ** 2
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
    if not isinstance (unknown_text_vector, list) \
            or not isinstance(known_text_vectors, list) \
            or not isinstance(language_labels, list) \
            or not isinstance(k, int):
        return None
    if len(language_labels) != len(known_text_vectors):
        return None
    calculate_distances = []
    for vector in known_text_vectors:
        calculate_distances.append(calculate_distance_sparse(unknown_text_vector, vector))
    distances = sorted(calculate_distances)[:k]
    sorted_languages = []
    for distance in distances:
        sorted_languages.append(language_labels[calculate_distances.index(distance)])
    list_of_label_and_distances = list(zip(sorted_languages, distances))
    list_of_label_and_distances = sorted(list_of_label_and_distances, key=lambda i: i[1])
    dict_of_label_and_distances = {}
    for pair in list_of_label_and_distances:
        if pair[0] in dict_of_label_and_distances.keys():
            dict_of_label_and_distances[pair[0]] += 1
        else:
            dict_of_label_and_distances[pair[0]] = 1
    common_languages = max(dict_of_label_and_distances, key= dict_of_label_and_distances.get)
    result = [common_languages, round(float(min(distances)),5)]
    return result

