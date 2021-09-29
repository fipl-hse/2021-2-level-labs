"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None
    for words in text:
        text = text.replace('\n', ' ')
        if words != ' ' and not words.isalpha():
            text = text.replace(words, '')
    return text.lower().split()


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not tokens:
        return None
    if not isinstance(stop_words, list) or not stop_words:
        return tokens
    for symbol in tokens:
        for symbol_stop in stop_words:
            if symbol in stop_words and symbol_stop in tokens:
                tokens.remove(symbol_stop)
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    freq_dict = {}
    for keys in tokens:
        if not isinstance(keys, str):
            return None
        if keys not in freq_dict:
            freq_dict.update({keys: 1})
        else:
            freq_dict.update({keys: tokens.count(keys)})
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    freq_dict = sorted(freq_dict, key = freq_dict.get, reverse=True)
    freq_dict = list(freq_dict)
    freq_dict = freq_dict[:top_n]
    return freq_dict


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str) or not isinstance(text, str)\
            or not isinstance(stop_words, list):
        return None
    freq_dict = calculate_frequencies(remove_stop_words(tokenize(text),
                                                                    stop_words))
    profile_lang = {'name': language,
                    'freq': freq_dict,
                    'n_words': len(freq_dict)}
    return profile_lang



def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict)\
            or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None
    cross = []
    for i in get_top_n_words(profile_to_compare['freq'], top_n):
        if i in get_top_n_words(unknown_profile['freq'], top_n):
            cross.append(i)
    cross = round((len(cross) / top_n), 2)
    return cross


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
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict)\
            or not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None
    if compare_profiles(unknown_profile, profile_1, top_n) >\
            compare_profiles(unknown_profile, profile_2, top_n):
        return profile_1['name']
    if compare_profiles(unknown_profile, profile_1, top_n) <\
            compare_profiles(unknown_profile, profile_2, top_n):
        return profile_2['name']
    if compare_profiles(unknown_profile, profile_1, top_n) ==\
            compare_profiles(unknown_profile, profile_2, top_n):
        fin_lang = sorted([profile_1['name'], profile_2['name']])
        return fin_lang[0]
    return None

def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict)\
        or not isinstance(top_n, int):
        return None
    cross = []
    for i in get_top_n_words(profile_to_compare['freq'], top_n):
        if i in get_top_n_words(unknown_profile['freq'], top_n):
            cross.append(i)
    length = 0
    for words in profile_to_compare['freq']:
        length += len(words)
    max_word = 0
    min_word = 0
    for max_length in profile_to_compare['freq']:
        if len(max_length) == max(map(len, profile_to_compare['freq'])):
            max_word = max_length
    for min_length in profile_to_compare['freq']:
        if len(min_length) == min(map(len, profile_to_compare['freq'])):
            min_word = min_length
    score = round((len(cross) / top_n), 2)
    lang_adv = {'name': profile_to_compare['name'],
                'common': cross,
                'score': score,
                'max_length_word': max_word,
                'min_length_word': min_word,
                'average_token_length': length / len(profile_to_compare['freq']),
                'sorted_common': sorted(cross)}

    return lang_adv



def detect_language_advanced(unknown_profile: dict, profiles: list,
                             languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profiles, list)
            and isinstance(languages, list)
            and isinstance(top_n, int)):
        return None
    lang_profile = []
    if not languages:
        lang_profile = profiles
    for profile in profiles:
        if profile['name'] in languages:
            lang_profile.append(profile)
    score = []
    for cross in lang_profile:
        score.append(compare_profiles_advanced(unknown_profile, cross, top_n))
    final = sorted(score, key=lambda lang_name: lang_name['name'])
    if len(final) >= 1:
        final = sorted(score, key=lambda cross_score: cross_score['score'], reverse=True)
    else:
        return None
    return final[0]['name']
