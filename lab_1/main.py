"""
Lab 1
Language detection
"""

import re
import json


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text,str):
        return None
    text2=text.lower()
    token = re.sub(r'[^\w\s\d+]','',text2)
    token2 = re.split(r'\s', token)
    for token in token2:
        if token == '':
            token2.remove(token)
    return token2


def remove_stop_words(token2: list, stop_words: list)-> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(token2, list) or not isinstance(stop_words, list):
        return None
    if token2:
        for token in enumerate(token2):
            if token[1] in stop_words:
                token2[token[0]] = ' '
        while ' ' in token2:
            token2.remove(' ')
        return token2
    return None

                    
def calculate_frequencies(token2: list)-> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(token2, list):
        return None
    for token in token2:
        if isinstance(token,str):
            freqdict = {}
            for x in token2:
                if x in freqdict:
                    freqdict[x]+=1
                else:
                    freqdict[x]=1
            return freqdict
        return None


def get_top_n_words(freqdict: dict, top_n:int)-> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freqdict, dict) or not isinstance(top_n, int):
        return None
    top_dict = dict(sorted(freqdict.items(), key=lambda kv: kv[1], reverse=True))
    freqdict = list(top_dict)
    return freqdict[:top_n]


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
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    frq_dict = calculate_frequencies(tokens)
    language_profile = {'name': language, 'freq': frq_dict, 'n_words': len(frq_dict)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict,
                     top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) \
            or not isinstance(top_n, int):
        return None
    top_n_words_unk = get_top_n_words(unknown_profile['freq'], top_n)
    top_n_words_comp = get_top_n_words(profile_to_compare['freq'], top_n)
    common_elements = 0
    for element in top_n_words_unk:
        if element in top_n_words_comp:
            common_elements += 1
    freq_common = common_elements / len(top_n_words_unk)
    return round(freq_common, 2)


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
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) \
            and isinstance(profile_2, dict) and isinstance(top_n, int):
        return None
    freq_common1 = compare_profiles(unknown_profile, profile_1, top_n)
    freq_common2 = compare_profiles(unknown_profile, profile_2, top_n)
    if freq_common1 > freq_common2:
        return profile_1['name']
    if freq_common2 > freq_common1:
        return profile_2['name']
    if freq_common1 == freq_common2:
        languages_names = [profile_1['name'], profile_2['name']]
        languages_names.sort()
    return languages_names[0]


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
    if not isinstance(unknown_profile, dict) \
            or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None
    name = profile_to_compare['name']
    common = []
    for word in enumerate(get_top_n_words(profile_to_compare['freq'], top_n)):
        if word[1] in get_top_n_words(unknown_profile['freq'], top_n):
            common.append(word[1])
    score = compare_profiles(unknown_profile, profile_to_compare, top_n)
    pr_words = list(profile_to_compare['freq'].keys())
    max_length_word = ''
    for maximum in enumerate(pr_words):
        if len(maximum[1]) > len(max_length_word):
            max_length_word = maximum[1]
    min_length_word = max_length_word
    for minimum in enumerate(pr_words):
        if len(minimum[1]) < len(min_length_word):
            min_length_word = minimum[1]
    all_letters = 0
    for letters in enumerate(pr_words):
        all_letters += len(letters[1])
    sort_common = common.copy()
    sort_common.sort()
    dict_adv = {'name': name,
                'common': common,
                'score': score,
                'max_length_word': max_length_word,
                'min_length_word': min_length_word,
                'average_token_length': all_letters / len(pr_words),
                'sorted_common': sort_common}
    return dict_adv


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
    if not isinstance(unknown_profile, dict) or not isinstance(profiles, list) \
            or not isinstance(languages, list) or not isinstance(top_n, int):
        return None
    prof_list = []
    for profile in profiles:
        if profile['name'] in languages or languages == []:
            profile_comp = compare_profiles_advanced(unknown_profile, profile, top_n)
            prof_list.append(profile_comp)
    if not prof_list:
        return None
    prof_list = sorted(prof_list, key=lambda x: x['score'], reverse=True)
    if len(prof_list) > 1:
        if prof_list[0]['score'] == prof_list[1]['score']:
            prof_common_score = []
            for element in prof_list:
                if element['score'] == prof_list[0]['score']:
                    prof_common_score.append(element)
            prof_list = sorted(prof_common_score, key=lambda x: x['score'], reverse=True)
    return prof_list[0]['name']


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str):
        return None
    try:
        with open(path_to_file, 'r', encoding='utf-8') as file:
            profile = json.load(file)
        return profile
    except FileNotFoundError:
        return None


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict):
        return 1
    with open('{}.json'.format(profile['name']), 'w', encoding='utf-8') as file:
        json.dump(profile, file)
    return 0
