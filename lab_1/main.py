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
    pass
    if not isinstance(text, str):
        return None
    text = text.lower()
    punktmarks = '''1234567890?!.,'"/\\<>{}[]():;-+=_@#№^|$%*'''
    for b in text:
        if b in punktmarks:
            text = text.replace(b, '')
    tokens = text.split()
    return tokens
    
def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    pass
    tokenlist = []
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    for b in tokens: 
        if b not in stop_words:
            tokenlist.append(b)
    return tokenlist
        


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    pass
    freq_dict = {}
    if not isinstance(tokens, list):
        return None
    for b in tokens:
        if type(b) != str:
            return None
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] = freq_dict[token]+1
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
    pass
    if isinstance(freq_dict, dict):
        sort = dict(sorted(freq_dict.items(), reverse=True, key=lambda x: x[1]))
        commonw = list(sort)
        commonw = commonw[:top_n]
        return commonw
    else:
        return None


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass
 
    if not isinstance(text, str):
        return None
    if not isinstance(stop_words, list):
        return None
    if not isinstance(language, str): 
        return None
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    language_profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    return language_profile
        
    
def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    pass
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(top_n, int):
        return None
    if not isinstance(profile_to_compare, dict):
        return None
    
    unknown_profile_tokens = get_top_n_words(unknown_profile['freq'], top_n)
    profile_to_compare_tokens = get_top_n_words(profile_to_compare['freq'], top_n)
    common_top_n = 0
    for i in unknown_profile_tokens:
        if i in profile_to_compare_tokens:
            common_top_n = common_top_n + 1
    distance = round(common_top_n/len(profile_to_compare_tokens))
    return distance

def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    pass
     if not isinstance(profile_1, dict):
        return None
    if not isinstance(profile_2, dict):
        return None
    if not isinstance(top_n, int):
        return None
    if not isinstance(unknown_profile, dict):
        return None
    
    compare_1 = compare_profiles(profile_1, unknown_profile, top_n)
    compare_2 = compare_profiles(profile_2, unknown_profile, top_n)
    name_1 = profile_1['name']
    name_2 = profile_2['name']
    
    if compare_1 > compare_2:
        return name_1
    if compare_2 > compare_1:
        return name_2
    if compare_1 == compare_2:
        names = [name_1, name_2]
        names = sorted(names)
        return names
   
  


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
