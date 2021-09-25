#coding=utf-8
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
    preprocessed = ''
    for i,v in enumerate(text):
        if v.isalnum() or v == ' ':
            preprocessed += v
    tokens = preprocessed.split()
    return tokens



def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
        Removes stop words
        :param tokens: a list of tokens
        :param stop_words: a list of stop words
        :return: a list of tokens without stop words
        """
    pass
    if not isinstance(tokens, list):
        return None
    if not isinstance(stop_words, list):
        return None
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
        Calculates frequencies of given tokens
        :param tokens: a list of tokens
        :return: a dictionary with frequencies
        """
    pass
    if not isinstance(tokens, list):
        return None
    for word in tokens:
        if not isinstance(word, str):
            return None
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    print (freq_dict)
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
            Returns the most common words
            :param freq_dict: a dictionary with frequencies
            :param top_n: a number of the most common words
            :return: a list of the most common words
            """
    pass
    if not isinstance(freq_dict, dict):
        return None
    if not isinstance(top_n, int):
        return None
    freq_dict = list(freq_dict.items())
    freq_dict_sort = sorted(freq_dict, key=lambda i: -i[1])
    if len(freq_dict_sort) == 0:
        return []
    new_freq_list = []
    for element in freq_dict_sort:
        new_freq_list.append(element[0])
        top_words = new_freq_list[:top_n]
    return top_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
        Creates a language profile
        :param language: a language
        :param text: a text
        :param stop_words: a list of stop words
        :return: a dictionary with three keys – name, freq, n_words
        """
    pass
    if not isinstance(language, str):
        return None
    if not isinstance(text, str):
        return None
    if len(text) == 0:
        return None
    if not isinstance(stop_words,list):
        return None
    profile = {}
    profile['name'] = language
    freq = calculate_frequencies(remove_stop_words(tokenize(text),stop_words))
    profile['freq'] = freq
    n_words = len(freq)
    profile['n_words'] = n_words

    return profile


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
    if not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None
    count = 0
    top_n_words_profile_to_compare = get_top_n_words(profile_to_compare['freq'],top_n)
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    len_top_n_words_unknown_profile = len(top_n_words_unknown_profile)
    if top_n_words_profile_to_compare == top_n_words_unknown_profile:
        share_of_common_frequency_words = float(1)
    else:
        for word_profile_to_compare in top_n_words_profile_to_compare:
            if word_profile_to_compare in top_n_words_unknown_profile:
                count += 1
        share_of_common_frequency_words = round(count / len_top_n_words_unknown_profile,2)
    return share_of_common_frequency_words


def detect_language(unknown_profile:dict, profile_1:dict, profile_2:dict, top_n:int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    pass
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profile_1,dict):
        return None
    share_of_common_words_with_profile_1 = compare_profiles(unknown_profile,profile_1,top_n)
    share_of_common_words_with_profile_2 = compare_profiles(unknown_profile,profile_2,top_n)
    if share_of_common_words_with_profile_1 > share_of_common_words_with_profile_2:
        return profile_1['name']
    elif share_of_common_words_with_profile_1 < share_of_common_words_with_profile_2:
        return profile_2 ['name']
    else:
        all_languages = [profile_1['name'], profile_2['name']]
        all_languages_sorted = all_languages.sort()
        return all_languages_sorted[0]


def compare_profiles_advanced(unknown_profile,profile_to_compare,top_n):
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    pass
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None
    profile_advanced = {}
    profile_advanced['name'] = profile_to_compare['name']
    top_n_words_profile_to_compare = get_top_n_words(profile_to_compare['freq'], top_n)
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    common_words = []
    for word_profile_to_compare in top_n_words_profile_to_compare:
        if word_profile_to_compare in top_n_words_unknown_profile:
            common_words.append(word_profile_to_compare)
    profile_advanced['common'] = common_words
    profile_advanced['score'] = compare_profiles(unknown_profile,profile_to_compare,top_n)
    freq_key_value = profile_to_compare['freq']
    list_words = []
    for word in freq_key_value.keys():
        list_words.append(word)
        max_length_word = max(list_words, key=len)
    profile_advanced['max_length_word'] = max_length_word
    profile_advanced['min_length_word'] = min(freq_key_value)
    len_values = len(freq_key_value)
    len_value = 0
    for value in freq_key_value:
        len_value += len(value)
    average_token_length = len_value / len_values
    profile_advanced['average_token_length'] = average_token_length
    sorted_common = sorted(common_words)
    profile_advanced['sorted_common'] = sorted_common
    return profile_advanced

def detect_language_advanced(unknown_profile, profiles, languages, top_n ):
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    pass
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profiles, list):
        return None
    if not isinstance(languages, list):
        return None
    if not isinstance(top_n, int):
        return None
    shares = {}
    if languages == []:
        for profile in profiles:
            language_profiles = compare_profiles_advanced(unknown_profile, profile, top_n)
            shares[language_profiles['name']] = language_profiles['score']
        sorted_dict = {}
        languages_with_max_value = []
        list_of_keys = list(shares.keys())
        list_of_values = list(shares.values())
        sorted_list = sorted(list_of_keys, reverse=False)
        for key_in_sorted_list in sorted_list:
            sorted_dict[key_in_sorted_list] = shares[key_in_sorted_list]
        max_value = max(list_of_values)
        for key_in_sorted_dict in sorted_dict.keys():
            if sorted_dict[key_in_sorted_dict] == max_value:
                languages_with_max_value.append(key_in_sorted_dict)
                language_with_max_value = languages_with_max_value[0]
    elif languages != []:
        for language in languages:
            for profile in profiles:
                if profile['name'] == language:
                    language_profiles = compare_profiles_advanced(unknown_profile, profile, top_n)
                    shares[language_profiles['name']] = language_profiles['score']
                    sorted_dict = {}
                    languages_with_max_value = []
                    list_of_keys = list(shares.keys())
                    list_of_values = list(shares.values())
                    sorted_list = sorted(list_of_keys, reverse=False)
                    for key_in_sorted_list in sorted_list:
                        sorted_dict[key_in_sorted_list] = shares[key_in_sorted_list]
                    max_value = max(list_of_values)
                    for key_in_sorted_dict in sorted_dict.keys():
                        if sorted_dict[key_in_sorted_dict] == max_value:
                            languages_with_max_value.append(key_in_sorted_dict)
                            language_with_max_value = languages_with_max_value[0]

    return language_with_max_value


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
