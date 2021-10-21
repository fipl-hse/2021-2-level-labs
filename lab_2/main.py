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
    if not isinstance(tokens, list) or None in tokens:
        return None
    frequency_dictionary = {}
    for word in tokens:
        frequency_dictionary[word] = round(tokens.count(word) / len(tokens), 5)
    return frequency_dictionary


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
    for text in texts_corpus:
        if not isinstance(text, list):
            return None
        freq_dict = get_freq_dict(text)
        language_profiles[language_labels[texts_corpus.index(text)]] = freq_dict
    return language_profiles


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(language_profiles, dict):
        return None
    unique_words = []
    for tokens in language_profiles.values():
        unique_words.extend(tokens)
    if not unique_words:
        return None
    unique_words.sort()
    return unique_words


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list) \
            or not isinstance(language_profiles, dict):
        return None
    text_vector = []
    text_features = get_language_features(language_profiles)
    for word in text_features:
        if word in original_text:
            for dictionary in language_profiles.values():
                if word in dictionary:
                    text_vector.append(dictionary[word])
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
    counter = 0
    for vector_value in unknown_text_vector:
        if not isinstance(vector_value, (int, float)) or not \
                isinstance(known_text_vector[counter], (int, float)):
            return None
        distance += (vector_value - known_text_vector[counter]) ** 2
        counter += 1
    return round(distance ** 0.5, 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not isinstance(unknown_text_vector, list) or not \
            isinstance(known_text_vectors, list) or not \
            isinstance(language_labels, list) or not \
            len(known_text_vectors) == len(language_labels):
        return None
    vectors_distances = []
    min_distance = []
    for known_text_vector in known_text_vectors:
        if not isinstance(known_text_vector, list):
            return None
        vectors_distances.append(calculate_distance(unknown_text_vector, known_text_vector))
    min_distance_vector = min(vectors_distances)
    min_distance.extend([language_labels[vectors_distances.index(min_distance_vector)], min_distance_vector])
    return min_distance


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    if not isinstance(unknown_text_vector, list) \
            or not isinstance(known_text_vector, list):
        return None
    for number in unknown_text_vector:
        if not isinstance(number, int) and not isinstance(number, float):
            return None
    for number in known_text_vector:
        if not isinstance(number, int) and not isinstance(number, float):
            return None
    distance = 0
    for num_unk, num_kn in zip(unknown_text_vector, known_text_vector):
        distance += abs(num_unk - num_kn)
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
    if not (
            isinstance(unknown_text_vector, list)
            and all(isinstance(n, (int, float)) for n in unknown_text_vector)
            and isinstance(known_text_vectors, list)
            and all(isinstance(m, list) for m in known_text_vectors)
            and isinstance(language_labels, list)
            and all(isinstance(s, str) for s in language_labels)
            and len(known_text_vectors) == len(language_labels)
    ):
        return None
    if metric == 'euclid':
        calc_dist = calculate_distance
    elif metric == 'manhattan':
        calc_dist = calculate_distance_manhattan
    distances = [calc_dist(unknown_text_vector, knw_vector) for knw_vector in known_text_vectors]
    sorted_distances = (sorted(distances))[:k]
    langs = [language_labels[distances.index(dist)] for dist in sorted_distances]
    langs = sorted(zip(langs, sorted_distances), key=lambda x: x[1])
    lang_count = {}
    for lang, _ in langs:
        if lang not in lang_count:
            lang_count[lang] = 0
        lang_count[lang] += 1
    return [max(lang_count, key=lang_count.get), min(sorted_distances)]
