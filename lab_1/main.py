"""Lab 1
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
    puncs = """'!@#$%^&*()-_=+/|"№;%:?><,.`~’…—[]{}1234567890\t"""
    for symbol in text:
        if symbol in puncs:
            text = text.replace(symbol, '')
    tokens = text.lower().split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not tokens:
        return None
    tokens_copy = list(tokens)
    for token in tokens:
        if token in stop_words:
            tokens_copy.remove(token)
    return tokens_copy


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    frequencies = {}
    if isinstance(tokens, list):
        for token in tokens:
            if not isinstance(token, str):
                return None
            elif not token in frequencies.keys():
                frequencies[token] = 1
            else:
                frequency = frequencies.get(token)
                frequency += 1
                frequencies.update({token: frequency})
        return frequencies


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        if not freq_dict.keys() or top_n <= 0:
            return []
        else:
            top_words = []
            freq_words = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
            for element in freq_words[:top_n]:
                top_words.append(element[0])
            return top_words


def create_language_profile(language: str,
                            text: str,
                            stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        freq_dict = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
        lang_profile = {'name': language,
                        'freq': freq_dict,
                        'n_words': len(freq_dict.keys())}
        return lang_profile


def compare_profiles(unknown_profile: dict,
                     profile_to_compare: dict,
                     top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int): #too long
        unknown_top_words = get_top_n_words(unknown_profile.get('freq'), top_n)
        compare_top_words = get_top_n_words(profile_to_compare.get('freq'), top_n)
        shared_top_words = [word for word in unknown_top_words if word in compare_top_words]
        shared_proportions = round(len(shared_top_words) / len(unknown_top_words), 2)
        return shared_proportions


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
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) and isinstance(profile_2, dict) and isinstance(top_n, int): #too long
        proportion_1 = compare_profiles(unknown_profile, profile_1, top_n)
        proportion_2 = compare_profiles(unknown_profile, profile_2, top_n)
        if proportion_1 > proportion_2:
            result_language = profile_1.get('name')
        elif proportion_1 < proportion_2:
            result_language = profile_2.get('name')
        else:
            languages = sorted([profile_1.get('name'), profile_2.get('name')])
            result_language = languages[0]
        return result_language


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None
    unknown_top_words = get_top_n_words(unknown_profile.get('freq'), top_n)
    compare_top_words = get_top_n_words(profile_to_compare.get('freq'), top_n)
    shared_top_words = [word for word in compare_top_words if word in unknown_top_words]
    shared_proportions = len(shared_top_words) / len(unknown_top_words)
    max_length_word = ''
    tokens_length = 0
    frequency = profile_to_compare.get('freq')
    for word in frequency.keys():
        if len(word) > len(max_length_word):
            max_length_word = word
    min_length_word = max_length_word
    for word in frequency.keys():
        if len(word) < len(min_length_word):
            min_length_word = word
        tokens_length += len(word)
    average_token_length = tokens_length / len(frequency.keys())
    report = {'name': profile_to_compare.get('name'),
              'common': shared_top_words,
              'score': shared_proportions,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted(shared_top_words)}
    return report


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
    if not isinstance(unknown_profile, dict) or not isinstance(profiles, list) or not isinstance(languages, list) or not isinstance(top_n, int):
        return None
    proportions = []
    languages_with_same_proportions = []
    if len(languages) > 0:
        check = False
        for language_name in languages:
            for language_profile in profiles:
                if language_name in language_profile.get('name'):
                    check = True
        if not check:
            return None
        for language_profile in profiles:
            if language_profile.get('name') in languages:
                proportion = compare_profiles_advanced(unknown_profile, language_profile, top_n)
                proportions.append([language_profile.get('name'), proportion.get('score')])
        for res in proportions[:-1]:
            if proportions[0][1] == proportions[proportions.index(res) + 1][1]:
                languages_with_same_proportions.append(proportions[proportions.index(res)][0])
        languages_with_same_proportions.sort()
        if len(languages_with_same_proportions) > 0:
            result = languages_with_same_proportions[0]
            return result
        proportions.sort(key=lambda x: x[1], reverse=True)
        result = proportions[0][0]
        return result
    for language_profile in profiles:
        proportion = compare_profiles_advanced(unknown_profile, language_profile, top_n)
        proportions.append([language_profile.get('name'), proportion.get('score')])
    for res in proportions[:-1]:
        if proportions[0][1] == proportions[proportions.index(res) + 1][1]:
            languages_with_same_proportions.append(proportions[proportions.index(res)][0])
    languages_with_same_proportions.sort()
    if len(languages_with_same_proportions) > 0:
        result = languages_with_same_proportions[0]
        return result
    proportions.sort(key=lambda x: x[1], reverse=True)
    result = proportions[0][0]
    return result


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str):
        return None
    try:
        with open(path_to_file, 'r', encoding='utf-8') as file_to_read:
            language_profile = json.load(file_to_read)
    except FileNotFoundError:
        return None
    return language_profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
