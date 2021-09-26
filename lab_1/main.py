"""
Lab 1
Language detection
"""
import json


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    invaluable_trash = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                        '.', '?', '/', '\t', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    if not isinstance(text, str):
        return None
    text = text.lower()
    for symbols in invaluable_trash:
        text = text.replace(symbols, '')
    tokens = text.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    new_tokens = []
    for word in tokens:
        if word not in stop_words:
            new_tokens.append(word)
    return new_tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    frequency_dictionary = {}
    if not isinstance(tokens, list):
        return None
    for word in tokens:
        if isinstance(word, str):
            if word in frequency_dictionary:
                frequency_dictionary[word] += 1
            else:
                frequency_dictionary[word] = 1
        else:
            return None
    return frequency_dictionary
# return dict e.g. {'assessment': 5, 'karina': 90, 'hello': 1, 'ship': 3}


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    freq_list = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    top_n_words = []
    # take the zero element of the tuples (it is the sorted tokens) and add to the new list
    for tuple_element in freq_list:
        top_n_words.append(tuple_element[0])
    # take the top_n tokens from the list of sorted tokens
    top_n_words = top_n_words[:top_n]
    return top_n_words
# return list e.g. ['karina', 'assessment']


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if (not isinstance(language, str)
            or not isinstance(text, str)
            or not isinstance(stop_words, list)):
        return None
    # use function remove_stop_words
    tokens = remove_stop_words(tokenize(text), stop_words)
    # use function calculate_frequencies
    frequency_dictionary = calculate_frequencies(tokens)
    # find the number of tokens in the dictionary
    n_words = len(frequency_dictionary.keys())
    # create language profile
    profile = {"name": language, "freq": frequency_dictionary, "n_words": n_words}
    return profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
    # use function get_top_n_words
    top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    # find common tokens
    common_things = list(set(top_n_words_unknown) & set(top_n_words_compare))
    # find share of common tokens
    share_of_common_things = round(len(common_things)/len(top_n_words_unknown), 2)
    return share_of_common_things


def detect_language(unknown_profile: dict,
                    profile_1: dict,
                    profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_1, dict)
            or not isinstance(profile_2, dict)
            or not isinstance(top_n, int)):
        return None
    # use function compare_profiles
    share_the_first_language = compare_profiles(unknown_profile, profile_1, top_n)
    share_the_second_language = compare_profiles(unknown_profile, profile_2, top_n)
    # detect the language via share of common tokens
    if share_the_first_language == share_the_second_language:
        if_two_language = sorted([profile_1["name"], profile_2["name"]])
        language_name = if_two_language[0]
    elif share_the_first_language > share_the_second_language:
        language_name = profile_1["name"]
    else:
        language_name = profile_2["name"]
    return language_name


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> dict or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
    # use function get_top_n_words to get common and sorted_common
    top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    common = []
    for word in top_n_words_compare:
        if word in top_n_words_unknown:
            common.append(word)
    # common = list(set(top_n_words_compare) & set(top_n_words_unknown)) I can't use this here:(
    sorted_common = sorted(common)
    # get score
    score = round(len(common) / len(top_n_words_unknown), 2)
    # get max and min length of words
    max_length_word = max(profile_to_compare["freq"].keys(), key=len)
    min_length_word = min(profile_to_compare["freq"].keys(), key=len)
    # get average_token_length via list with length of tokens
    length_of_tokens = []
    for token in profile_to_compare["freq"].keys():
        length_of_tokens.append(len(token))
    average_token_length = sum(length_of_tokens)/len(profile_to_compare["freq"].keys())
    # get a report
    report = {'name': profile_to_compare["name"],
              'common': common,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted_common}
    return report


def detect_language_advanced(unknown_profile: dict,
                             profiles: list,
                             languages: list,
                             top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profiles, list)
            or not isinstance(languages, list)
            or not isinstance(top_n, int)):
        return None
    # sort the reports by score
    reports = []
    for profile in profiles:
        if profile["name"] in languages or not languages:
            report = compare_profiles_advanced(unknown_profile, profile, top_n)
            reports.append(report)
    reports = sorted(reports, key=lambda x: x["score"], reverse=True)
    # sort in alphabetically order if some languages have the same max scores
    if len(reports) == 0:
        return None
    if len(reports) > 1:
        if reports[0]["score"] == reports[1]["score"]:
            reports_with_max_score = []
            for element in reports:
                if element["score"] == reports[0]["score"]:
                    reports_with_max_score.append(element)
            reports = sorted(reports_with_max_score, key=lambda x: x["name"])
    language = reports[0]["name"]
    return language


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str):
        return None
    # load profile from file
    try:
        with open(path_to_file, "r", encoding="utf-8") as json_file:
            profile = json.load(json_file)
    except FileNotFoundError:
        return None
    return profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict) or ("name" or "freq" or "n_words") not in profile.keys():
        return 1
    if (not isinstance(profile["name"], str)
            or not isinstance(profile["freq"], dict)
            or not isinstance(profile["n_words"], int)):
        return 1
    # generate file name from profile name
    path_to_file = "{}.json".format(profile["name"])
    # save profile in json file
    with open(path_to_file, "w", encoding="utf-8") as file:
        json.dump(profile, file)
    return 0
