"""
Lab 1
Language detection
"""


import re
def tokenize(text):
    while isinstance(text, str):
        tokens = []
        contemp_string = ''
        text = text.lower()
        text = re.sub(r'[^\w\s]','', text)
        text = text.split()
        for token in text:
            if token.isalpha() or token.isdigit():
                tokens.append(token)
            elif token.isalnum():
                for symbol in token:
                    if symbol.isalpha():
                        contemp_string += symbol
                tokens.append(contemp_string)
                contemp_string = ''
        return tokens
    else:
        return None


def remove_stop_words(tokens, stop_words):
    tokens_without_stopwords = []
    for token in tokens:
        while not isinstance(token, str):
            return None
        else:
            continue
    if stop_words == []:
        return tokens
    else:
        for word in stop_words:
            while not isinstance(word, str):
                return tokens
            else:
                continue
    for token in tokens:
        if not token in stop_words:
            tokens_without_stopwords.append(token)
    return tokens_without_stopwords


def calculate_frequencies(tokens):
    freq_dict = {}
    while isinstance(tokens, list):
        for token in tokens:
            while isinstance(token, str):
                if token in freq_dict:
                    value = freq_dict[token]
                    freq_dict[token] = value + 1
                else:
                    freq_dict[token] = 1
            else:
                return None
    else:
        return None
    return freq_dict


def get_top_n_words(freq_dict, top_n):
    while isinstance(freq_dict, dict) and isinstance(top_n, int):
        freq_dict_sorted = {}
        values = list(freq_dict.values())
        keys = list(freq_dict.keys())
        sorted_values = sorted(freq_dict.values(), reverse = True)
        if sorted_values == [sorted_values[0]] * len(sorted_values):
            freq_dict_sorted = freq_dict
        else:
            for v in sorted_values:
                for k in freq_dict.keys():
                    if freq_dict[k] == v:
                        freq_dict_sorted[k] = v

        if not freq_dict_sorted == {}:
            values = list(freq_dict_sorted.values())
            keys = list(freq_dict_sorted.keys())
            sorted_values = sorted(freq_dict_sorted.values(), reverse = True)
            if sorted_values == [sorted_values[0]] * len(sorted_values): #same frequency check
                if top_n >= len(sorted_values):
                    return keys
                elif top_n < len(sorted_values):
                    keys = keys[:top_n]
                    return keys     
            else:
                values = list(freq_dict_sorted.values())
                keys = list(freq_dict_sorted.keys())
                if top_n > len(values):
                    return keys
                else:
                    keys = keys[:top_n]
                    return keys
        else:
            keys = []
            return keys
    else:
        return None


def create_language_profile(language, text, stop_words):
    if type(language) == str and type(text) == str and type(stop_words) == list:
        language_profile = {}
        language_profile['name'] = language
    
        tokens = tokenize(text)
        tokensWithoutStopWords = remove_stop_words(tokens, stop_words)
        freq = calculate_frequencies(tokensWithoutStopWords)

    
        language_profile['freq'] = freq
        language_profile['n_words'] = len(freq)

        return language_profile
    else:
        return None


def compare_profiles(unknown_profile, profile_to_compare, top_n):
    if type(unknown_profile) == dict and type(profile_to_compare) == dict and type(top_n) == int:
        freq_list_up = unknown_profile['freq']
        top_n_up = get_top_n_words(freq_list_up, top_n)

        freq_list_ptc = profile_to_compare['freq']
        top_n_ptc = get_top_n_words(freq_list_ptc, top_n)

        profiles_in_common = []
        for n in top_n_up:
            if n in top_n_ptc:  
                profiles_in_common.append(n)
        compare_profiles = len(profiles_in_common) / len(top_n_up)
        return compare_profiles
    else:
        return None

def detect_language(unknown_profile, profile_1, profile_2, top_n):
    if type(unknown_profile) == dict and type(profile_1) == dict and type(profile_2) == dict and type(top_n) == int:
        compare_1 = compare_profiles(unknown_profile, profile_1, top_n)
        compare_2 = compare_profiles(unknown_profile, profile_2, top_n)
        if compare_1 > compare_2:
            return profile_1['name']
        elif compare_2 > compare_1:
            return profile_2['name']
        else:
            return max(profile_1['name'], profile_2['name']) 


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
