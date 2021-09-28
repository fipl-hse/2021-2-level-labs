"""
Lab 1
Language detection
"""
import json
from os.path import exists


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None
    for symbol in text:
        if not (symbol.isalpha() or symbol.isspace()):
            text = text.replace(symbol, '')
    text = text.lower().split()
    return text


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not (
        isinstance(tokens, list)
        and tokens != []
        and all(isinstance(s, str) for s in tokens)
    ):
        return None
    if isinstance(stop_words, list):
        cleaned_tokens = []
        for token in tokens:
            if token not in stop_words:
                cleaned_tokens.append(token)
        return cleaned_tokens
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not (
        isinstance(tokens, list)
        and all(isinstance(s, str) for s in tokens)
    ):
        return None
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
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
    if not (
        isinstance(freq_dict, dict)
        and all(isinstance(v, int) for v in freq_dict.values())
        and isinstance(top_n, int)
    ):
        return None
    srtd_list = sorted(freq_dict, key=freq_dict.get, reverse=True)
    if top_n < len(srtd_list):
        return srtd_list[:top_n]
    return srtd_list


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not (
        isinstance(language, str)
        and isinstance(text, str)
        and isinstance(stop_words, list)
    ):
        return None
    tokens = tokenize(text)
    cleaned_tokens = remove_stop_words(tokens, stop_words)
    freq_dict_chaos = calculate_frequencies(cleaned_tokens)
    freq_list = sorted(freq_dict_chaos, key=freq_dict_chaos.get, reverse=True)
    freq_dict_srtd = {}
    for i in freq_list:
        freq_dict_srtd[i] = freq_dict_chaos[i]
    language_profile = {'name': language, 'freq': freq_dict_srtd, 'n_words': len(freq_dict_srtd)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not (
        isinstance(unknown_profile, dict)
        and isinstance(profile_to_compare, dict)
        and isinstance(top_n, int)
    ):
        return None
    first_top_n = get_top_n_words(unknown_profile['freq'], top_n)
    second_top_n = get_top_n_words(profile_to_compare['freq'], top_n)
    profiles_in_common = []
    for wrd in first_top_n:
        if wrd in second_top_n:
            profiles_in_common.append(wrd)
    result = round(len(profiles_in_common) / len(first_top_n), 2)
    return result


def detect_language(unknown_profile: dict,
                    first_profile: dict,
                    second_profile: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not (
        isinstance(unknown_profile, dict)
        and isinstance(first_profile, dict)
        and isinstance(second_profile, dict)
        and isinstance(top_n, int)
    ):
        return None
    first_compare = compare_profiles(unknown_profile, first_profile, top_n)
    second_compare = compare_profiles(unknown_profile, second_profile, top_n)
    if first_compare > second_compare:
        return first_profile['name']
    if second_compare > first_compare:
        return second_profile['name']
    return sorted(first_profile['name'], second_profile['name'])


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
    if not (
        isinstance(unknown_profile, dict)
        and isinstance(profile_to_compare, dict)
        and isinstance(top_n, int)
    ):
        return None
    top_words_unk = get_top_n_words(unknown_profile['freq'], top_n)
    top_words_comp = get_top_n_words(profile_to_compare['freq'], top_n)
    common_words = []
    for word in top_words_comp:
        if word in top_words_unk:
            common_words.append(word)
    score = compare_profiles(unknown_profile, profile_to_compare, top_n)
    tokens = profile_to_compare['freq'].keys()
    max_length_word = max(tokens, key=len)
    min_length_word = min(tokens, key=len)
    all_tokens_len = len(''.join(tokens))
    average_token_length = all_tokens_len / len(tokens)
    sorted_common = sorted(common_words)
    report = {'name': profile_to_compare["name"],
              'common': common_words,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted_common}
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
    if not (
        isinstance(unknown_profile, dict)
        and isinstance(profiles, list)
        and isinstance(languages, list)
        and isinstance(top_n, int)
    ):
        return None
    dict_lang_score = {}
    for profile_to_compare in profiles:
        if profile_to_compare["name"] in languages or not languages:
            compare = compare_profiles_advanced(unknown_profile, profile_to_compare, top_n)
            dict_lang_score[compare['name']] = compare['score']
    if dict_lang_score:
        sorted_lang = []
        for lang, score in dict_lang_score.items():
            if score == max(dict_lang_score.values()):
                sorted_lang.append(lang)
        sorted_lang = sorted(sorted_lang)
    else:
        return None
    return sorted_lang[0]


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not (
        isinstance(path_to_file, str)
        and exists(path_to_file)
    ):
        return None
    with open(path_to_file, mode='r', encoding='UTF-8') as file:
        profile = json.load(file)
        return profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not (
        isinstance(profile, dict)
        or isinstance(profile['name'], str)
        or isinstance(profile['freq'], dict)
        or isinstance(profile['n_words'], int)
    ):
        return 1
    profile_dict = '{}.json'.format(profile['name'])
    with open(profile_dict, mode='w', encoding='UTF-8') as file:
        json.dump(profile, file)
        return 0
