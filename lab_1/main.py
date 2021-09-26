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
    if isinstance(text, str):
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
    if isinstance(tokens, list) and isinstance(stop_words, list):
        for word in tokens:
            if word not in stop_words:
                tokens_update.append(word)
        return tokens_update

    return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    freq = {}
    if isinstance(tokens, list):
        for word in tokens:
            if isinstance(word, str):
                if word in list(freq.keys()):
                    freq[word] += 1
                else:
                    freq[word] = 1
            else:
                return None
        return freq
    return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        most_common = []
        chart = sorted(list(freq_dict.values()), reverse=True)
        chart = chart[:top_n]
        freq_dict_temp = dict(freq_dict)
        for i in chart:
            word = list(freq_dict_temp.keys())[list(freq_dict_temp.values()).index(i)]
            most_common.append(word)
            freq_dict_temp.pop(word)
        return most_common
    return None


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
        if text_tmp is not None:
            if language.isalpha():
                lan_profile = {"name": language}
                lan_profile["freq"] = text_tmp
                lan_profile["n_words"] = len(lan_profile["freq"])
                print(lan_profile)
            return lan_profile
        return None
    except AttributeError:
        return None


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
    except TypeError:
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
    try:
        p1_cross = compare_profiles(unknown_profile, profile_1, top_n)
        p2_cross = compare_profiles(unknown_profile, profile_2, top_n)

        if p1_cross > p2_cross:
            return profile_1["name"]
        if p2_cross > p1_cross:
            return profile_2["name"]
        alphabetical = sorted(list[profile_1["name"], profile_2["name"]])
        return alphabetical[0]

    except TypeError:
        return None


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
    stats = {}
    try:
        top_unknown = get_top_n_words(unknown_profile["freq"], top_n)
        top_compare = get_top_n_words(profile_to_compare["freq"], top_n)
        stats["name"] = profile_to_compare["name"]

        cross = 0
        stats["common"] = []
        for token in top_compare:
            if token in top_unknown:
                cross += 1
                stats["common"].append(token)

        stats["score"] = round(cross / top_n, 2)

        stats["sorted_common"] = sorted(stats["common"])
        tokens_length = 0
        max_l = len(list(profile_to_compare["freq"].keys())[0])
        min_l = max_l
        for word in profile_to_compare["freq"]:
            if len(word) >= max_l:
                stats["max_length_word"] = word
            if len(word) <= min_l:
                stats["min_length_word"] = word
            tokens_length += len(word)
        tokens_number = len(profile_to_compare["freq"])
        stats["average_token_length"] = tokens_length / tokens_number
        return stats
    except TypeError:
        return None


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
    try:
        if not languages:
            languages = profiles.copy()
        count = 0
        score_best = 0
        profile = profiles[count]
        score_best_name = profile["name"]
        for language in languages:
            if isinstance(language, dict):
                language = language["name"]
            if language == profile["name"]:
                score_current = compare_profiles_advanced(unknown_profile, profile, top_n)["score"]
            if score_current > score_best:
                score_best_name = language
                score_best = score_current
            elif score_current == score_best:
                compare = sorted([score_best_name, language])
                score_best_name = compare[0]
            count += 1
            try:
                profile = profiles[count]
            except IndexError:
                pass
        return score_best_name
    except (UnboundLocalError, TypeError):
        return None
