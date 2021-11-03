"""
Lab 2
Language classification
"""
from math import sqrt, fabs
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
    # Check for bad input
    if not isinstance(tokens, list):
        return None
    if not elements_instances(tokens, str):
        return None
    # Iterate over tokens, recording their count in a dictionary
    count = {}
    for token in tokens:
        if token not in count:
            count[token] = 0
        count[token] += 1
    # Convert the counts to frequencies in the range from 0 to 1
    # Round the frequencies, which is apparently required by the tests
    return {k: round(v / len(tokens), 5) for k, v in count.items()}


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    # Check for bad input
    if (not isinstance(texts_corpus, list)
            or not isinstance(language_labels, list)):
        return None
    if (not elements_instances(texts_corpus, list)
            or not elements_instances(language_labels, str)):
        return None
    # Generate a dictionary mapping labels onto freq_dicts of texts
    return {k: get_freq_dict(v) for k, v in zip(language_labels, texts_corpus)}


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    # Check for bad input
    if not isinstance(language_profiles, dict):
        return None
    # Extract all lists of words from profiles
    texts = [freq_dict.keys() for freq_dict in language_profiles.values()]
    if not texts:
        return None
    # Convert lists of words to sets, combine them and sort alphabetically
    return sorted(set().union(*texts))


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    # Check for bad input
    if not isinstance(original_text, list):
        return None
    if not elements_instances(original_text, str):
        return None
    # Get features
    features = get_language_features(language_profiles)
    # By casting the word list to a set, membership checks
    # are improved from O(n) to O(1) on average
    original_text = set(original_text)
    # "Combine" language profiles into one, using the max values
    max_scores = {word: 0 for word in features}
    for profile in language_profiles.values():
        for word, score in profile.items():
            if score > max_scores[word] and word in original_text:
                max_scores[word] = score
    # Return vector using data from combined dictionary
    return [max_scores[word] for word in features]


# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    # Check for bad input
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vector, list)):
        return None
    if not elements_instances(unknown_text_vector + known_text_vector, int, float):
        return None
    # Pythagoras
    distance = sum((a-b)**2 for a, b in zip(unknown_text_vector, known_text_vector))**0.5
    # Explicitly cast to float and round, because apparently necessary
    return round(float(distance), 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    # Check for bad input
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
    # Get a list of distances comparing unknown vector and known vectors
    scores = [calculate_distance(unknown_text_vector, vector) for vector in known_text_vectors]
    # Return a [label, score] with the lowest score
    return list(min(zip(language_labels, scores), key=lambda x: x[1]))


# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    # Check for bad input
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vector, list)):
        return None
    if not elements_instances(unknown_text_vector + known_text_vector, int, float):
        return None
    # Manhattan
    distance = sum(abs(a-b) for a, b in zip(unknown_text_vector, known_text_vector))
    # Explicitly cast to float and round, because apparently necessary
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
    # Check for bad input
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vectors, list)
            or not isinstance(language_labels, list)
            or not isinstance(k, int)
            or not isinstance(metric, str)):
        return None
    if len(known_text_vectors) != len(language_labels):
        return None
    # Choose the appropriate distance function
    distance = calculate_distance_manhattan if metric == "manhattan" else calculate_distance
    # Get a list of distances comparing unknown vector and known vectors
    scores = [distance(unknown_text_vector, vector) for vector in known_text_vectors]
    # Choose K nearest neighbours (label, score)
    best_fits = sorted(zip(language_labels, scores), key=lambda x: x[1])[:k]
    # Count label occurences and record them in a dictionary
    label_freq = {}
    for label, _ in best_fits:
        if label not in label_freq:
            label_freq[label] = 0
        label_freq[label] += 1
    # Return label with highest occurence, and lowest score
    return [max(label_freq, key=label_freq.get), min(scores)]


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    # Check for bad input
    if not isinstance(original_text, list):
        return None
    if not elements_instances(original_text, str):
        return None
    # Get features
    features = get_language_features(language_profiles)
    # By casting the word list to a set, membership checks
    # are improved from O(n) to O(1) on average
    original_text = set(original_text)
    # "Combine" language profiles into one, using the max values
    max_scores = {word: 0 for word in features}
    for profile in language_profiles.values():
        for word, score in profile.items():
            if score > max_scores[word] and word in original_text:
                max_scores[word] = score
    # Return sparse vector using data from combined dictionary
    return [[i, max_scores[word]] for i, word in enumerate(features) if word in original_text]


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    # Check for bad input
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vector, list)):
        return None
    if (not elements_instances(unknown_text_vector, list)
            or not elements_instances(unknown_text_vector, list)):
        return None
    # Convert vectors into dictionaries, with indices being keys
    unknown_text_dict = dict(unknown_text_vector)
    known_text_dict = dict(known_text_vector)
    # Combine dictionaries
    combined = {**unknown_text_dict, **known_text_dict}
    # If an index appeared in both dictionaries,
    # the combined value is the difference of values
    for index in combined:
        if index in unknown_text_dict and index in known_text_dict:
            combined[index] = unknown_text_dict[index] - known_text_dict[index]
    # Pythagoras
    distance = sum(d**2 for d in combined.values())**0.5
    # Explicitly cast to float and round, because apparently necessary
    return round(float(distance), 5)


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
    # Check for bad input
    if (not isinstance(unknown_text_vector, list)
            or not isinstance(known_text_vectors, list)
            or not isinstance(language_labels, list)
            or not isinstance(k, int)):
        return None
    if len(known_text_vectors) != len(language_labels):
        return None
    # Get a list of distances comparing unknown vector and known vectors
    scores = [calculate_distance_sparse(unknown_text_vector, vector)
              for vector in known_text_vectors]
    # Choose K nearest neighbours (label, score)
    best_fits = sorted(zip(language_labels, scores), key=lambda x: x[1])[:k]
    # Count label occurences and record them in a dictionary
    label_freq = {}
    for label, _ in best_fits:
        if label not in label_freq:
            label_freq[label] = 0
        label_freq[label] += 1
    # Return label with highest occurence, and lowest score
    return [max(label_freq, key=label_freq.get), min(scores)]
