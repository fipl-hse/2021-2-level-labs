"""
Lab 1
Language detection
"""
import string


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
        :param text: a text
        :return: a list of lower-cased tokens without punctuation
    """
    text_new = ""
    if type(text) == str:
        for i in text:
            if i not in string.punctuation:
                text_new += i
    else:
        return None

    text_new = text_new.lower()
    text_new = text_new.split()

    return text_new


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    tokens_update = []

    try:
        if type(tokens) == list and type(stop_words) == list:
            for word in tokens:
                if word not in stop_words:
                    tokens_update.append(word)

            return tokens_update
        else:
            return None
    except:
        return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    freq = {}
    if type(tokens) == list:
        for word in tokens:
            if type(word) == str:
                if word in list(freq.keys()):
                    freq[word] += 1
                else:
                    freq[word] = 1
            else:
                return None
        return freq
    else:
        return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    try:
        most_common = []
        chart = sorted(list(freq_dict.values()), reverse=True)
        chart = chart[:top_n]
        freq_dict_temp = dict(freq_dict)
        for i in chart:
            word = list(freq_dict_temp.keys())[list(freq_dict_temp.values()).index(i)]
            most_common.append(word)
            freq_dict_temp.pop(word)
    except:
        return None

    return most_common


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    try:
        text_tmp = text
        text_tmp = tokenize(text_tmp)
        text_tmp = remove_stop_words(text_tmp, stop_words)
        text_tmp = calculate_frequencies(text_tmp)
        if text_tmp != None:
            if language.isalpha():
                lan_profile = {"name": language}
                lan_profile["freq"] = text_tmp
                lan_profile["n_words"] = len(lan_profile["freq"])
                print(lan_profile)
        else:
            return None
    except:
        return None

    return lan_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    try:
        n_unknown = get_top_n_words(unknown_profile["freq"], top_n)
        n_compare = get_top_n_words(profile_to_compare["freq"], top_n)
        cross = 0
        for token in n_compare:
            if token in n_unknown:
                cross += 1

        return round(cross / top_n, 2)
    except:
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
    try:
        p1_cross = compare_profiles(unknown_profile, profile_1, top_n)
        p2_cross = compare_profiles(unknown_profile, profile_2, top_n)

        if p1_cross > p2_cross:
            return profile_1["name"]
        elif p2_cross > p1_cross:
            return profile_2["name"]
        else:
            alphabetical = list[profile_1["name"], profile_2["name"]].sorted()
            return alphabetical[0]

    except:
        return None


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    try:
        top_unknown = get_top_n_words(unknown_profile, top_n)
        top_compare = get_top_n_words(profile_to_compare, top_n)
        cross =
    except:
        return None

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
