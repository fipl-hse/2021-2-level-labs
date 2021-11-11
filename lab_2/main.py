def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None
    text = text.lower()
    preprocessed = ''
    for symbol in text:
        if symbol.isalnum() or symbol == ' ':
            preprocessed += symbol
    tokens = preprocessed.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    for word in tokens:
        if not isinstance(word, str):
            return None
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1/len(tokens)
        else:
            freq_dict[token] = 1/len(tokens)

    for i in freq_dict:
        freq_dict[i] = round(freq_dict[i], 5)

    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    if not isinstance(texts_corpus, list) or not isinstance(language_labels, list):
        return None

    for i in texts_corpus:
        if i is None:
            return None

        for j in i:
            if not isinstance(j, str):
                return None

    for i in language_labels:
        if not isinstance(i, str):
            return None

    profiles = dict()
    for i in range(len(language_labels)):
        profiles[language_labels[i]] = get_freq_dict(texts_corpus[i])
    return profiles


def get_language_features(language_profiles: dict) -> list or None:
    if not isinstance(language_profiles, dict) or len(language_profiles) == 0:
        return None
    features = list()
    for profile in language_profiles:
        features += language_profiles[profile].keys()
    return sorted(features)


def get_text_vector1(original_text: list, language_profiles: dict) -> list or None:
    if not isinstance(language_profiles, dict) or not isinstance(original_text, list):
        return None

    text_vector = list()
    for text in original_text:
        text_in_profile = list()
        for profile in language_profiles:
            if text in language_profiles[profile]:
                text_in_profile.append(language_profiles[profile][text])
            else:
                text_in_profile.append(0)
        text_vector.append(max(text_in_profile))
    return text_vector


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    if not isinstance(language_profiles, dict) or not isinstance(original_text, list):
        return None

    text_vector = list()
    for text in get_language_features(language_profiles):
        if text in original_text:
            for profile in language_profiles:
                if text in language_profiles[profile]:
                    text_vector.append(language_profiles[profile][text])
        else:
            text_vector.append(0)
    return text_vector


def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    if not isinstance(known_text_vector, list) or not isinstance(unknown_text_vector, list):
        return None

    for i in unknown_text_vector:
        if i != 0:
            if not isinstance(i, float):
                return None

    for i in known_text_vector:
        if i != 0:
            if not isinstance(i, float):
                return None
    s = 0
    for i in range(len(unknown_text_vector)):
        s += (unknown_text_vector[i] - known_text_vector[i]) ** 2
    return round(s ** 0.5, 5)


def predict_language_score(unknown_text_vector: list, known_text_vectors: list, language_labels: list) -> [str, int]\
                                                                                                          or None:
    if not isinstance(known_text_vectors, list) or not isinstance(unknown_text_vector, list) or\
            not isinstance(language_labels, list) or len(language_labels) != len(known_text_vectors):
        return None
    for i in unknown_text_vector:
        if i != 0:
            if not isinstance(i, float):
                return None
    for i in known_text_vectors:
        for j in i:
            if j != 0:
                if not isinstance(j, float):
                    return None
    for i in language_labels:
        if not isinstance(i, str):
            return None

    best_result = 0
    label = ""
    for i in range(len(known_text_vectors)):
        calc = calculate_distance(unknown_text_vector, known_text_vectors[i])
        if i == 0:
            best_result = calc
            label = language_labels[i]
        if calc <= best_result:
            best_result = calc
            label = language_labels[i]
    return [label, best_result]


def calculate_distance_manhattan(unknown_text_vector: list, known_text_vector: list) -> float or None:
    if not isinstance(known_text_vector, list) or not isinstance(unknown_text_vector, list):
        return None
    for i in unknown_text_vector:
        if i != 0:
            if not isinstance(i, float):
                return None
    for i in known_text_vector:
        if i != 0:
            if not isinstance(i, float):
                return None
    s = 0
    # print(len(known_text_vector), len(unknown_text_vector))
    for i in range(min(len(known_text_vector), len(unknown_text_vector))):
        s += abs(unknown_text_vector[i] - known_text_vector[i])
    return round(s, 5)


def predict_language_knn(unknown_text_vector: list, known_text_vectors: list, language_labels: list, k=1,
                         metric='manhattan') -> [str, int] or None:
    if not isinstance(known_text_vectors, list) or not isinstance(unknown_text_vector, list) or \
            not isinstance(language_labels, list) or len(known_text_vectors) != len(language_labels):
        return None
    for i in unknown_text_vector:
        if i != 0:
            if not isinstance(i, float):
                return None
    for j in known_text_vectors:
        for i in j:
            if i != 0:
                if not isinstance(i, float):
                    return None

    res = list()
    for i in range(len(known_text_vectors)):
        if metric == 'manhattan':
            calc = calculate_distance_manhattan(unknown_text_vector, known_text_vectors[i])
        else:
            calc = calculate_distance(unknown_text_vector, known_text_vectors[i])
        res.append([calc, language_labels[i]])
        # print([calc, language_labels[i]], i)
    # print(res)
    res = sorted(res, key=lambda x: x[0])[:k]
    # print(res)

    scores = dict()
    for i in res:
        if i[1] in scores:
            scores[i[1]] += 1
        else:
            scores[i[1]] = 1

    for i in scores:
        if scores[i] == max(scores.values()):
            lbl = i
            break

    return [lbl, res[0][0]]

    for i in res:
        if i[1] == lbl:
            return [lbl, i[0]]
