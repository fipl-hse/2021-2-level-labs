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
    if isinstance(text,str) != True:
        return None
    text = text.lower()
    for symbol in text:
        if symbol in '''1234567890!@#$%^&*()_-+={}[]|\\'";://?>.<,№%`~''':   # А как работать с символами, которых у нас нет на клавиатуре?
            text = text.replace(symbol, '')                                  #Например, с математическими знаками?
    tokens = text.split()                                                    #Почему проверка через ifalpha не может использоваться?
    for token in tokens:
        token.strip()
    return tokens



def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not (isinstance(tokens, list) and isinstance(stop_words, list)):
        return None       #for word in tokens:
    without_sw = []       #if word in stop_words:
    for token in tokens:  #tokens.remove(word) - Почему не работает?
        if token not in stop_words:
            without_sw.append(token)
    return without_sw




def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if isinstance(tokens,list) != True:
        return None
    t_dict = {}
    for word in tokens:
        if isinstance(word,str) and word in t_dict.keys():
            t_dict[word] += 1
        elif isinstance(word,str) and word not in t_dict.keys():
            t_dict[word] = 1
    if t_dict == {}:
        return None
    return t_dict



def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not (isinstance(freq_dict, dict) and isinstance(top_n, int)):
        return None
    top = []
    if top_n > len(freq_dict):
        top_n = len(freq_dict)
    freq_dict = sorted(freq_dict.items(), key=lambda x: (-x[1], x[0]))
    for i in range(top_n):
        top.append(freq_dict[i][0])
    return top



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
    l_profile = {}
    l_profile['name'] = language
    l_profile['freq'] = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
    l_profile['n_words'] = len(l_profile['freq'])
    return l_profile



def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not (isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int)):
        return None
    match = 0
    top_1 = get_top_n_words(unknown_profile['freq'], top_n)
    top_2 = get_top_n_words(profile_to_compare['freq'], top_n)
    for word in top_1:
        if word in top_2:
            match += 1
    return round(match / top_n, 2)



def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not (isinstance(unknown_profile, dict) and isinstance(profile_1, dict) and isinstance(profile_2, dict) and isinstance(top_n, int)):
        return None
    detect_dict = {}
    detect_dict[compare_profiles(profile_1, unknown_profile, top_n)] = profile_1['name']
    detect_dict[compare_profiles(profile_2, unknown_profile, top_n)] = profile_2['name']
    return detect_dict[max(detect_dict.keys())]



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
