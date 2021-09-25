#coding=utf-8
"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words list
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if type(text) != str:
        return None
    text = text.lower()
    marks = '''!()-[]{};?@#$%:'"/,.\\^&*_<>'''
    for x in text:
        if x in marks:
            text = text.replace(x,'')
    tokens = text.split()
    return tokens

    pass


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    tokens_1 = []
    if type(stop_words) != list:
        return None
    if type(tokens) != list:
        return None
    for token in tokens:
        if token not in stop_words:
            tokens_1.append(token)
    print(tokens_1)
    return tokens_1

    pass
stop_words = ['the', 'a', 'is']

def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    freqs_dict = {}
    if type(tokens) != list:
        return None
    for token in tokens:
        if type(token) != str:
            return None
        if token not in freqs_dict:
            freqs_dict[token] = 1
        else:
            freqs_dict[token] += 1
    return (freqs_dict)

    pass


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if type(freq_dict) != dict:
        return None
    freq_dict = sorted(freq_dict.items(), key=lambda x:-x[1])
    if len(freq_dict) == 0:
        return []
    freq_2_dict = list()
    for word in freq_dict:
        freq_2_dict.append(word[0])
    return list(freq_2_dict[:top_n])

    pass


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if len(text) == 0:
        return None
    if type(stop_words) != list:
        return None
    if type(language) != str:
        return None
    profile = {}
    profile ['name'] = language
    new_tokenization = tokenize(text)
    new_remove_stop_words = remove_stop_words(new_tokenization, stop_words)
    profile['freq'] = calculate_frequencies(new_remove_stop_words)
    profile['n_words'] = len(profile['freq'])
    return profile

    pass


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if not isinstance (top_n,int) :
        return None
    new_freq_dict = unknown_profile['freq']
    new_get_top_n_words = get_top_n_words(new_freq_dict, top_n)
    new_freq_dict_2 = profile_to_compare['freq']
    new_get_top_n_words_2 = get_top_n_words(new_freq_dict_2, top_n)
    common_words = 0
    for word in new_get_top_n_words:
        if word in new_get_top_n_words_2:
            common_words += 1
    proportion_of_frequency = round(common_words/top_n, 2)
    return proportion_of_frequency

    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) or not isinstance (profile_2, dict) :
        return None
    if not isinstance (top_n,int) :
        return None
    proportion_of_frequency_1 = compare_profiles(unknown_profile, profile_1, top_n)
    proportion_of_frequency_2 = compare_profiles(unknown_profile, profile_2, top_n)
    list = [profile_1['name'], profile_2 ['name']]
    list_1 = list.sort()
    if proportion_of_frequency_1 > proportion_of_frequency_2:
        return profile_1 ['name']
    elif proportion_of_frequency_2 > proportion_of_frequency_1:
        return profile_2 ['name']
    else:
        return list_1[0]

    pass


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if not isinstance (top_n,int) :
        return None
    profile = {}
    new_get_top_n_words_1 = get_top_n_words(unknown_profile['freq'], top_n)
    new_get_top_n_words_2 = get_top_n_words (profile_to_compare['freq'], top_n)
    common_words = []
    for word in new_get_top_n_words_1:
        if word in new_get_top_n_words_2:
            common_words.append(word)
    profile['common'] = common_words
    score = 0
    for word_1 in new_get_top_n_words_1:
        if word_1 in new_get_top_n_words_2:
            score +=1
    proportion_of_frequency = round (score/top_n, 2)
    profile ['score'] = proportion_of_frequency
    tokens = list(profile_to_compare['freq'].keys())
    max_length_word = max(tokens, key=len)
    min_length_word = min (tokens, key = len)
    profile['max_length_word'] = max_length_word
    profile ['min_length_word'] = min_length_word
    number_of_letters = 0

    for word_2 in tokens:
        number_of_letters += len(word_2)
    number_of_words = len(tokens)
    average_token_length = number_of_letters/number_of_words
    profile ['average_token_length'] = average_token_length
    common_words.sort()
    profile['sorted_common'] = common_words
    if proportion_of_frequency > 0:
        profile ['name'] = profile_to_compare ['name']
    else:
        profile['name'] = unknown_profile ['name']
    return profile
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
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance (profiles,list):
        return None
    if not isinstance (languages, list):
        return None
    if not isinstance(top_n, int):
        return None
    dict_languages_and_scores = {}
    for profile in profiles:
        if len(languages) == 0 or profile['name'] in languages:
            profile_3 = compare_profiles_advanced (unknown_profile, profile, top_n)
            score_1 = profile_3['score']
            dict_languages_and_scores[profile['name']] = score_1
    sorted_dict_languages_and_scores = sorted(dict_languages_and_scores.items(), key = lambda x: x[1])
    if len(sorted_dict_languages_and_scores) == 0:
        return None
    common_profiles = list()
    highest_score = sorted_dict_languages_and_scores[len(sorted_dict_languages_and_scores)-1][1]
    for language in sorted_dict_languages_and_scores:
        if language[1] >= highest_score:
            common_profiles.append(language[0])


    common_profiles.sort()
    return common_profiles [0]


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
