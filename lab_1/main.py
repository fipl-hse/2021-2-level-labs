"""
Lab 1
Language detection
"""

import re


def tokenize(text: str) -> list or None:
    if isinstance(text, str):
        text = text.lower()
        text = text.replace("'", "")
        text = text.replace("\n", " ")
        text = re.sub(r"[#%!@&*><.]", "", text)
        text = re.sub(r"[^a-zāūīōēȳüßöä]+", " ", text)
        text = re.sub(r'\s+', ' ', text)
        text = ' '.join(text.split())
        tokens = text.split(" ")
        return tokens
    else:
        return None


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    try:
        for i in tokens:
            if isinstance(i, str):
                tokens = [i for i in tokens if i not in stop_words]
                return tokens
            else:
                return None
    except:
        return None


def calculate_frequencies(tokens: list) -> dict or None:
    print(tokens)
    if type(tokens) is list:
        for i in tokens:
            if isinstance(i, str):
                freq_dict = {i: tokens.count(i) for i in tokens}
                return freq_dict
            else:
                return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        if freq_dict != {} and top_n > 0:
            new_dict = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
            count = 1
            top_list = []
            first, snd = zip(*new_dict)
            for i in first:
                if count <= top_n:
                    top_list.append(i)
                    count += 1
                if count > top_n:
                    break
            return top_list
        else:
            return []
    else:
        return None


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    first_step = tokenize(text)
    second_step = remove_stop_words(first_step, stop_words)
    freq_dict = calculate_frequencies(second_step)
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        language_profile = {"name": language,
                            "freq": freq_dict,
                            "n_words": len(freq_dict)}
        return language_profile
    else:
        return None


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        top_n_common_words = []
        top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
        top_n_words_known_profile = get_top_n_words(profile_to_compare['freq'],top_n)
        for i in top_n_words_unknown_profile:
            if i in top_n_words_known_profile:
                top_n_common_words.append(i)
        intersecting_words = len(top_n_common_words)/len(top_n_words_unknown_profile)
        return round(float(intersecting_words), 2)
    else:
        return None



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
