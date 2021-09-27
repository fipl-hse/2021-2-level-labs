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
    word = []
    tokens = []
    for i in text.lower():
        if i.isalpha():
            word.append(i)
        elif i.isspace():
            if word:
                tokens.append(''.join(word))
            word = []
    if len(word) > 0:
        tokens.append(''.join(word))
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if (not isinstance(tokens, list) or not isinstance(stop_words, list)
            or not all(isinstance(i, str) for i in tokens)):
        return None
    tokens = [i for i in tokens if i not in stop_words]
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if not isinstance(tokens, list) or not all(isinstance(i, str) for i in tokens):
        return None
    freq_dict = {}
    for i in tokens:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
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
    top_words = []
    if all(isinstance(e, str) for e in list(freq_dict.keys())):
        top_words = sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]
    return top_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not (isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list)):
        return None
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    n_words = len(freq_dict)
    language_profile = dict(name=language, freq=freq_dict, n_words=n_words)
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    if not (isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None
    common = []
    unknown = get_top_n_words(unknown_profile.get('freq'), top_n)
    compare = get_top_n_words(profile_to_compare.get('freq'), top_n)
    for i in unknown:
        if i in compare:
            common.append(i)
    distance = round(len(common) / len(unknown), 2)
    return distance


def detect_language(unknown_profile: dict, profile_1: dict,
                    profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """

    if not (isinstance(unknown_profile, dict) and isinstance(profile_1, dict)
            and isinstance(profile_2, dict) and isinstance(top_n, int)):
        return None
    first = compare_profiles(unknown_profile, profile_1, top_n)
    second = compare_profiles(unknown_profile, profile_2, top_n)
    if first > second:
        language = profile_1.get('name')
    elif first < second:
        language = profile_2.get('name')
    else:
        language = sorted([profile_1.get('name'), profile_2.get('name')])[0]
    return language


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict,
                              top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """

    if not (isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None
    common = []
    tokens = list(profile_to_compare.get('freq').keys())
    max_length_word = max(tokens, key=len)
    min_length_word = min(tokens, key=len)
    unknown = get_top_n_words(unknown_profile.get('freq'), top_n)
    compare = get_top_n_words(profile_to_compare.get('freq'), top_n)
    for i in compare:
        if i in unknown:
            common.append(i)
    score = len(common) / len(compare)
    whole_len = 0
    for i in tokens:
        whole_len += len(i)
    average_token_length = whole_len / len(tokens)
    sorted_common = sorted(common)
    language_profile = {'name': profile_to_compare.get('name'),
                        'common': common,
                        'score': score,
                        'max_length_word': max_length_word,
                        'min_length_word': min_length_word,
                        'sorted_common': sorted_common,
                        'average_token_length': average_token_length}
    return language_profile


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list,
                             top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """

    if not (isinstance(unknown_profile, dict) and isinstance(profiles, list)
            and isinstance(languages, list) and isinstance(top_n, int)):
        return None
    score = {}
    exist_lang = False
    for _ in profiles:
        if languages:
            for i in languages:
                if i == _.get('name'):
                    exist_lang = True
                    score[i] = compare_profiles_advanced(unknown_profile, _, top_n).get('score')
        else:
            score[_.get('name')] = compare_profiles_advanced(unknown_profile, _, top_n).get('score')
    if not exist_lang and languages:
        return None
    sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)
    i = 0
    first_score = sorted_score[0][1]
    name_list = []
    while i < len(sorted_score) and first_score == sorted_score[i][1]:
        name_list.append(sorted_score[i][0])
        i += 1
    name_list_sorted = sorted(name_list)
    return name_list_sorted[0]


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not isinstance(path_to_file, str):
        return None
    try:
        with open(path_to_file, 'r', encoding='utf-8') as json_file:
            lang_profile = json.load(json_file)
    except FileNotFoundError:
        return None
    return lang_profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """

    if not isinstance(profile, dict):
        return 1
    if ('name' or 'freq' or 'n_words') not in profile.keys():
        return 1
    lang_file = profile.get('name') + '.json'
    with open(lang_file, 'w', encoding='utf-8') as lang_profile:
        json.dump(profile, lang_profile)
    return 0
