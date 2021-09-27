"""
Lab 1
Language detection
"""
import json


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

    if not isinstance(text, str):
        return None

    punctuation_symbols = '''!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~'''
    for punctuation_symbol in punctuation_symbols:
        text = text.replace(punctuation_symbol, "")

    text = text.lower()
    return text.split()


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if not isinstance(stop_words, list) or not isinstance(tokens, list):
        return None

    clean_list = []

    for token in tokens:
        if token not in stop_words:
            clean_list.append(token)

    return clean_list


def calculate_frequencies(tokens: list) -> dict or None:
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
        if token in freq_dict.keys():
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1

    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    if not isinstance(freq_dict, dict):
        return None

    freq_dict = sorted(freq_dict.items(), key=lambda x: -x[1])
    if not freq_dict:
        return []
    top_words, _ = zip(*freq_dict)

    return list(top_words[:top_n])


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not text or not isinstance(language, str) or not isinstance(stop_words, list):
        return None

    tokenized_list = tokenize(text)
    clean_tokenized_list = remove_stop_words(tokenized_list, stop_words)

    profile_dict = {'name': language, 'freq': calculate_frequencies(clean_tokenized_list)}
    profile_dict['n_words'] = len(profile_dict['freq'])

    return profile_dict


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None

    unknown_profile_top_words = get_top_n_words(unknown_profile['freq'], top_n)
    profile_to_compare_top_words = get_top_n_words(profile_to_compare['freq'], top_n)

    number_of_matches = 0

    for word in unknown_profile_top_words:
        if word in profile_to_compare_top_words:
            number_of_matches += 1

    return round(number_of_matches / top_n, 2)


def detect_language(unknown_profile: dict,
                    profile_1: dict,
                    profile_2: dict,
                    top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) \
            or not isinstance(profile_2, dict) or not isinstance(profile_2, dict):
        return None

    profile_1_match = compare_profiles(unknown_profile, profile_1, top_n)
    profile_2_match = compare_profiles(unknown_profile, profile_2, top_n)

    result_name = ''

    if profile_1_match == profile_2_match:
        if profile_1['name'] < profile_2['name']:
            result_name = profile_1['name']
        else:
            result_name = profile_2['name']
    elif profile_1_match > profile_2_match:
        result_name = profile_1['name']
    else:
        result_name = profile_2['name']

    return result_name


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> dict or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) \
            or not isinstance(top_n, int):
        return None

    result_dict = {}

    match_score = compare_profiles(unknown_profile, profile_to_compare, top_n)

    if match_score > 0:
        result_dict['name'] = profile_to_compare['name']
    else:
        result_dict['name'] = unknown_profile['name']

    common = []

    unknown_profile_top_words = get_top_n_words(unknown_profile['freq'], top_n)
    profile_to_compare_top_words = get_top_n_words(profile_to_compare['freq'], top_n)

    for word in unknown_profile_top_words:
        if word in profile_to_compare_top_words:
            common.append(word)

    result_dict['common'] = common

    result_dict['score'] = match_score

    tokens = list(profile_to_compare['freq'].keys())
    max_length_word = tokens[0]
    for token in tokens:
        if len(token) > len(max_length_word):
            max_length_word = token
    result_dict['max_length_word'] = max_length_word

    min_length_word = tokens[0]
    for token in tokens:
        if len(token) < len(min_length_word):
            min_length_word = token
    result_dict['min_length_word'] = min_length_word

    overall_token_length = 0
    for token in tokens:
        overall_token_length += len(token)
    result_dict['average_token_length'] = overall_token_length / len(tokens)

    common.sort()
    result_dict['sorted_common'] = common

    return result_dict


def detect_language_advanced(unknown_profile: dict,
                             profiles: list,
                             languages: list,
                             top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """

    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profiles, list):
        return None
    if not isinstance(top_n, int):
        return None

    languages_match_scores = {}

    for profile in profiles:
        if not languages or profile['name'] in languages:
            match_score = compare_profiles_advanced(unknown_profile, profile, top_n)['score']
            languages_match_scores[profile['name']] = match_score

    languages_match_scores_sorted = sorted(languages_match_scores.items(), key=lambda x: -x[1])

    if languages_match_scores_sorted:
        identical_match_scores = []
        highest_score = languages_match_scores_sorted[0][1]
        for language_match_tuple in languages_match_scores_sorted:
            if language_match_tuple[1] == highest_score:
                identical_match_scores.append(language_match_tuple[0])

        identical_match_scores.sort()
        return identical_match_scores[0]

    return None


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not isinstance(path_to_file, str):
        return None

    try:
        with open(path_to_file, encoding="utf-8") as file:
            json_object = json.load(file)
    except FileNotFoundError:
        return None

    profile = {'name': json_object['name'],
               'freq': json_object['freq'],
               'n_words': json_object['n_words']}
    return profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """

    if not isinstance(profile, dict):
        return 1

    with open('../lab_1/profiles/' + profile['name'] + '.json', 'w', encoding="utf-8") as file:
        json.dump(profile, file)
    return 0
