"""
Lab 1
Language detection
"""


def tokenize(text: str):
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if isinstance(text, str) is False:
        return None
    symbols = ["'", ',', '.', '!', '?', '@', '#', '$', '%', '&', '*', '<',
                   '>', ';', ':', '-','=','+','_']
    for i in text:
        if i in symbols:
            text = text.replace(i, "")
    text1 = ''.join([i for i in text if not i.isdigit()])
    tokens = text1.lower().split()
    return tokens

def remove_stop_words(tokens, stop_words):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(tokens, list) and isinstance(stop_words, list):
        clean_text = [x for x in tokens if x not in stop_words]
        return clean_text
    return None


def calculate_frequencies(clean_text) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if isinstance(clean_text,list) and all(i for i in clean_text):
        freq = []
        for i in clean_text:
            word_count = clean_text.count(i)
            freq.append((i, word_count))
        freq_dict = dict(freq)
        return freq_dict
    return None


def get_top_n_words(freq_dict, top_n):
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    list_output = sorted(freq_dict, key=freq_dict.get, reverse=True)
    return list_output[:top_n]


def create_language_profile(language: str, text: str,
                            stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(language, str) and isinstance(text, str) \
            and isinstance(stop_words, list):
        language_profile = {}
        tokens = tokenize(text)
        tokens = remove_stop_words(tokens, stop_words)
        dict = calculate_frequencies(tokens)
        language_profile['name'] = language
        language_profile['freq'] = dict
        language_profile['n_words'] = len(language_profile['freq'].keys())
        return language_profile
    return None


def compare_profiles(unknown_profile: dict, profile_to_compare: dict,
                     top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        common_tokens = 0
        unknown_top_n_words = get_top_n_words(unknown_profile['freq'], top_n)
        compare_top_n_words = get_top_n_words(profile_to_compare['freq'], top_n)
        for word_1 in unknown_top_n_words:
            for word_2 in compare_top_n_words:
                if word_1 == word_2:
                    common_tokens += 1
        distance = round(common_tokens / top_n, 2)
        return distance
    return None


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
    if not isinstance(unknown_profile,dict) or not isinstance(profile_1,dict) \
            or not isinstance(profile_2,dict) or not isinstance(top_n,int):
        return None
    compare_1 = compare_profiles(unknown_profile,profile_1,top_n)
    compare_2 = compare_profiles(unknown_profile, profile_2, top_n)
    if compare_1 > compare_2:
        language = profile_1['name']
        return language
    elif compare_1 < compare_2:
        language = profile_2['name']
        return language
    elif compare_1 == compare_2:
        language = sorted(profile_1['name'], profile_2['name'])
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
    if not isinstance(unknown_profile, dict) or not \
            isinstance(profile_to_compare,dict) or not isinstance(top_n,int):
        return None
    unknown_top_n_words = get_top_n_words(unknown_profile["freq"], top_n)
    compare_top_n_words = get_top_n_words(profile_to_compare["freq"], top_n)
    common_words = []
    for i in compare_top_n_words:
        if i in unknown_top_n_words:
            common_words.append(i)
    token_length = []
    for token in profile_to_compare["freq"].keys():
        token_length.append(len(token))
    average_token_length = sum(token_length) / len(profile_to_compare["freq"].keys())
    language_profile = {'name': profile_to_compare["name"],
              'common': common_words,
              'score': round(len(common_words) / len(unknown_top_n_words), 2),
              'max_length_word': max(profile_to_compare["freq"].keys(), key=len),
              'min_length_word': min(profile_to_compare["freq"].keys(), key=len),
              'average_token_length': average_token_length,
              'sorted_common': sorted(common_words)}
    return language_profile


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
