"""
Lab 1
Language detection
"""

import re

def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if isinstance(text,str):
        smbl_in_txt = ''
        text = text.lower()
        for symbol in text:
            if symbol.isalpha() == True or symbol == ' ' or symbol == '\n':
                smbl_in_txt += symbol
        tokens = re.findall(r'\w+', smbl_in_txt)
        for token in tokens:
            if token == 'º':
                tokens.remove(token)
        return tokens
    return None


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(tokens,list) and isinstance(stop_words,list):
        meaningful_tokens = []
        for token in tokens:
            if token not in stop_words:
                meaningful_tokens.append(token)
        return meaningful_tokens
    return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if isinstance(tokens,list):
        freq_dict = {}
        for token in tokens:
            if type(token) != str:
                return None
            if token not in freq_dict:
                freq_dict[token] = 1
            else:
                freq_dict[token] += 1
        return freq_dict
    return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if isinstance(freq_dict,dict) and isinstance(top_n,int):
        n_dict = {k: freq_dict[k] for k in sorted(freq_dict, key=freq_dict.get, reverse=True)}
        top_lst = list(n_dict.keys())
        top = top_lst[:top_n]
        return top
    return None



def create_language_profile(language, text, stop_words):
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(language,str) and isinstance(text,str) and isinstance(stop_words,list):
        tokens = tokenize(text)
        meaningful_tokens = remove_stop_words(tokens, stop_words)
        f_dict = {}
        f_dict = calculate_frequencies(meaningful_tokens)
        lng_profile = {'name': language, 'freq': f_dict, 'n_words': len(f_dict)}
        return lng_profile
    return None


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict)\
            and isinstance(top_n, int):
        for k in unknown_profile.keys():
            if k == 'freq':
                d_unknown = unknown_profile['freq']
        for k in profile_to_compare.keys():
            if k == 'freq':
                d_compare = profile_to_compare['freq']
        top_unknown = get_top_n_words(d_unknown, top_n)
        top_compare = get_top_n_words(d_compare, top_n)
        equal = 0
        for k_u in top_unknown:
            for k_c in top_compare:
                if k_u == k_c:
                    equal += 1
        eq_per = round((equal / len(top_unknown)), 2)
        return eq_per
    return None


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict)\
            and isinstance(profile_2, dict) and isinstance(top_n, int):
        eq_per_1 = compare_profiles(unknown_profile, profile_1, top_n)
        eq_per_2 = compare_profiles(unknown_profile, profile_2, top_n)
        if eq_per_1 > eq_per_2:
            detected_language = profile_1.get('name')
        elif eq_per_2 > eq_per_1:
            detected_language = profile_2.get('name')
        return detected_language
    return None


#def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """



#def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """



#def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """


#def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
