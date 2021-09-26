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
    tokens = ''
    for i in text:
        if i.isalpha() or i.isspace():
            tokens += i

    tokens = tokens.lower().split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not (isinstance(stop_words, list) and isinstance(tokens, list)):
        return None
    tokens_new = []
    for i in tokens:
        if i not in stop_words:
            tokens_new.append(i)
    return tokens_new


def calculate_frequencies(tokens_new: list) -> dict or None:
    """
   Calculates frequencies of given tokens
   :param tokens: a list of tokens
   :return: a dictionary with frequencies
   """
    if not (isinstance(tokens_new, list) and isinstance(tokens_new[0], str)):
        return None
    freq_dict = {}
    for i in tokens_new:
        if i not in freq_dict:
            freq_dict[i] = 1
        else:
            freq_dict[i] += 1
    return freq_dict



def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not (isinstance(freq_dict, dict) and isinstance(top_n, int)):
        return None
    if top_n <= 0:
        return []
    top_n_words = []
    if top_n > len(freq_dict):
        top_n = len(freq_dict)
    freq_dict_copy = freq_dict.copy()
    top_n_copy = top_n
    while top_n_copy != 0:
        max_value = max(freq_dict_copy.values())
        for key, value in freq_dict_copy.items():
            if value == max_value:
                max_key = key
                break
        top_n_words.append(max_key)
        del freq_dict_copy[max_key]
        top_n_copy -= 1
    return top_n_words

def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    freq_dict = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
    if not (isinstance(language, str) and isinstance(freq_dict, dict)):
        return None
    language_profile = {'name': language,
                        'freq': freq_dict,
                        'n_words': len(freq_dict)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    top_n_words_profile_to_compare = get_top_n_words(profile_to_compare['freq'], top_n)
    common = []
    for i in top_n_words_unknown_profile:
        if i in top_n_words_profile_to_compare:
            common.append(i)
    return round(len(common) / len(top_n_words_unknown_profile), 2)


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
    percentage_1 = compare_profiles(unknown_profile, profile_1, top_n)
    percentage_2 = compare_profiles(unknown_profile, profile_2, top_n)
    if not (isinstance(percentage_1, float) and isinstance(percentage_2, float)):
        return None
    if percentage_1 > percentage_2:
        return profile_1['name']
    if percentage_1 < percentage_2:
        return profile_2['name']
    return [profile_1['name'], profile_2['name']].sort()[0]


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
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    top_n_words_profile_to_compare = get_top_n_words(profile_to_compare['freq'], top_n)
    common = []
    for i in top_n_words_profile_to_compare:
        if i in top_n_words_unknown_profile:
            common.append(i)
    score = float(len(common) / len(top_n_words_unknown_profile))
    sorted_common = sorted(common)
    sorted_tokens = sorted(list(profile_to_compare['freq'].keys()), key=len)
    min_length_word = sorted_tokens[0]
    max_length_word = sorted_tokens[-1]
    common_length = 0
    for i in sorted_tokens:
        common_length += len(i)
    average_token_length = common_length/len(sorted_tokens)
    report = {'name': profile_to_compare['name'], 'common': common, 'score': score,
              'max_length_word': max_length_word, 'min_length_word': min_length_word,
              'average_token_length': average_token_length, 'sorted_common': sorted_common}
    return report

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
    if not(isinstance(unknown_profile, dict) and isinstance(profiles, list)
           and isinstance(languages, list) and isinstance(top_n, int)):
        return None
    reports = []
    for current_profile in profiles:
        if current_profile['name'] in languages or not languages:
            reports.append(compare_profiles_advanced(unknown_profile, current_profile, top_n))
    if not reports:
        return None
    reports = sorted(reports, key=lambda k: k['score'], reverse=True)
    # to put languages in alphabetical score if there are some similar scores
    counter = 0
    for i in range(len(reports)-1):
        if reports[i]['score'] == reports[i+1]['score']:
            counter += 1
        else:
            break
    if counter != 0:
        language = sorted([reports[i]['name'] for i in range(0, counter+1)])[0]
    else:
        language = reports[0]['name']
    return language

def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str) or not exists(path_to_file):
        return None
    with open(path_to_file, encoding='utf-8') as file:
        profile = json.load(file)
    if profile:
        return profile
    return None



def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict) or ('name' or 'freq' or 'n_words') not in profile.keys():
        return 1
    if not (isinstance(profile['name'], str) and isinstance(profile['freq'], dict)
            and isinstance(profile['n_words'], int)):
        return 1
    new_file = "{}.json".format(profile['name'])
    with open(new_file, 'w', encoding='utf-8') as file:
        json.dump(profile, file)
    return 0
