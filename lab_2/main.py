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
    new_vector = [vec for vec in vector.values()]
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
    if not isinstance(unknown_text_vector, list) or not isinstance(known_text_vector, list):
        return None
    for el_unknown_vector in unknown_text_vector:
        if not isinstance(el_unknown_vector, (float, int)):
            return None
    for el_known_vector in known_text_vector:
        if not isinstance(el_known_vector, (float, int)):
            return None
    distance = 0
    for i in range(len(unknown_text_vector)):
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
            or not isinstance(language_labels, list):
        return None
    all_distance = []
    for vectors in known_text_vectors:
        if not isinstance(vectors,list) or len(language_labels) != len(known_text_vectors):
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
