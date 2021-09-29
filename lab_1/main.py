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
    if not isinstance(text, str):
        return None
    text_new = ""
    for i in text:
        if i not in string.punctuation:
            text_new += i

    return text_new.lower().split()


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not (isinstance(tokens, list) and isinstance(stop_words, list)):
        return None

    tokens_update = []
    for word in tokens:
        if word not in stop_words:
            tokens_update.append(word)
    return tokens_update


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    freq = {}
    if not isinstance(tokens, list):
        return None
    for word in tokens:
        if not isinstance(word, str):
            return None
        if word in list(freq.keys()):
            freq[word] += 1
        else:
            freq[word] = 1

    return freq


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    if not isinstance(freq_dict, dict) and isinstance(top_n, int):
        return None

    most_common = []
    sorted_freqs = sorted(freq_dict.values(), reverse=True)
    for freq in sorted_freqs:
        for k, val in freq_dict.items():
            if val == freq:
                most_common.append(k)

    most_common = list(dict.fromkeys(most_common))

    return most_common[:top_n]


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    # line too long so split in two
    if not isinstance(language, str) or not isinstance(text, str):
        return None
    if not isinstance(stop_words, list):
        return None

    text_tmp = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
    lan_profile = {"name": language, "freq": text_tmp, "n_words": len(text_tmp)}

    return lan_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(profile_to_compare, dict) or not isinstance(unknown_profile, dict):
        return None
    if not isinstance(top_n, int):
        return None

    n_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    n_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    cross = 0
    for token in n_compare:
        if token in n_unknown:
            cross += 1

    return round(cross / top_n, 2)


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
    # the check are divided in order to avoid long lines
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict):
        return None
    if not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None

    first_cross = compare_profiles(unknown_profile, profile_1, top_n)
    second_cross = compare_profiles(unknown_profile, profile_2, top_n)

    if first_cross > second_cross:
        return profile_1["name"]
    if second_cross > first_cross:
        return profile_2["name"]

    return sorted(list[profile_1["name"], profile_2["name"]])[0]


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict,
                              top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common,
    max_length_word, min_length_word, average_token_length
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None

    top_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_compare = get_top_n_words(profile_to_compare["freq"], top_n)

    cross = 0
    common = []
    for token in top_compare:
        if token in top_unknown:
            cross += 1
            common.append(token)

    tokens_length = 0
    max_l = len(list(profile_to_compare["freq"].keys())[0])
    min_l = max_l
    for word in profile_to_compare["freq"]:
        if len(word) >= max_l:
            max_w = word
        if len(word) <= min_l:
            min_w = word
        tokens_length += len(word)

    stats = {"name": profile_to_compare["name"],
             "score": round(cross / top_n, 2),
             "common": common,
             "sorted_common": sorted(common),
             "min_length_word": min_w,
             "max_length_word": max_w,
             "average_token_length": tokens_length / len(profile_to_compare["freq"])}
    return stats


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
    # obvious type checks
    if not isinstance(unknown_profile, dict) or not isinstance(profiles, list):
        return None

    # checks given languages - if none then all profiles are used
    if not languages:
        languages = profiles.copy()
    # counter will go through profiles
    count = 0
    # best score and current score are created; for best score also name is taken
    score_best = 0
    score_best_name = profiles[count]["name"]
    score_current = 0
    # helps with non existent language bad input
    check = True
    for language in languages:
        # the current profile is taking which will be compared
        profile = profiles[count]
        # prevents errors when only one language is needed
        if isinstance(language, dict):
            language = language["name"]
        # current score comparison with the current profile is created
        # if this if wasn't entered then the language isn't in profiles => None returned
        if language == profile["name"]:
            score_current = compare_profiles_advanced(unknown_profile, profile, top_n)["score"]
            check = False
        # updates best score and name if necessary
        if score_current > score_best:
            score_best_name = language
            score_best = score_current
        # if score is the same as the best - the names are alphabetically compared
        elif score_current == score_best:
            compare = sorted([score_best_name, language])
            score_best_name = compare[0]
        count += 1

    if check:
        return None

    return score_best_name
