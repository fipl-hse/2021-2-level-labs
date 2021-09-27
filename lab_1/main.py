"""
Lab 1
Language detection
"""

import json
from os.path import exists


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    # Check for bad input
    if not isinstance(text, str):
        return None

    # Remove non-alphabetic characters
    text = ''.join([i for i in text if i.isalpha() or i.isspace()])

    # Convert to lowercase and split into tokens
    return text.lower().split()


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    # Check for bad input
    if not isinstance(tokens, list) or not tokens:
        return None
    if not isinstance(stop_words, list):
        return tokens

    # Remove stop words from tokens
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    # Check for bad input
    if not isinstance(tokens, list):
        return None

    # Record the frequency of tokens in a dictionary
    frequencies = {}
    for token in tokens:
        # Check for bad list contents
        if not isinstance(token, str):
            return None

        if token not in frequencies:
            frequencies[token] = 0
        frequencies[token] += 1
    return frequencies


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    # Check for bad input
    if (not isinstance(freq_dict, dict)
            or not isinstance(top_n, int)):
        return None
    # Sort the frequency dictionary keys by their values
    # Return the top n keys
    return sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]


def create_language_profile(language: str,
                            text: str,
                            stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    # Check for bad input
    if (not isinstance(language, str)
            or not isinstance(text, str)
            or not isinstance(stop_words, list)):
        return None
    # Get frequencies
    tokens = remove_stop_words(tokenize(text), stop_words)
    frequencies = calculate_frequencies(tokens)
    # Get n_words
    n_words = len(frequencies.keys())
    # Assemble language profile
    return {"name": language, "freq": frequencies, "n_words": n_words}


def compare_profiles(unknown_profile: dict,
                     profile_to_compare: dict,
                     top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    # Check for bad input
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
    # Get sets of top N tokens of given profiles
    compare_top = set(get_top_n_words(profile_to_compare["freq"], top_n))
    unknown_top = set(get_top_n_words(unknown_profile["freq"], top_n))
    # Find set of shared tokens
    shared = compare_top.intersection(unknown_top)
    # Find distance between profiles
    distance = round(len(shared) / len(unknown_top), 2)
    return distance


def detect_language(unknown_profile: dict,
                    profile_1: dict,
                    profile_2: dict,
                    top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    # Check for bad input
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_1, dict)
            or not isinstance(profile_2, dict)
            or not isinstance(top_n, int)):
        return None
    distance_1 = compare_profiles(unknown_profile, profile_1, top_n)
    distance_2 = compare_profiles(unknown_profile, profile_2, top_n)
    if distance_1 == distance_2:
        if profile_1["name"] < profile_2["name"]:
            return profile_1["name"]
        return profile_2["name"]
    if distance_1 > distance_2:
        return profile_1["name"]
    return profile_2["name"]


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    # Check for bad input
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
    # Find common words, while preserving the order
    unknown_top = get_top_n_words(unknown_profile["freq"], top_n)
    compare_top = get_top_n_words(profile_to_compare["freq"], top_n)
    common = [token for token in compare_top if token in unknown_top]
    # Sort common words alphabetically
    sorted_common = sorted(common)
    # Find score
    score = len(common) / len(compare_top)
    # Token length
    tokens = [token for token, freq in profile_to_compare["freq"].items()]
    min_length_word = min(tokens, key=len)
    max_length_word = max(tokens, key=len)
    average_token_length = sum(map(len, tokens)) / len(tokens)
    # Assemble report
    report = {"name": profile_to_compare["name"],
              "common": common,
              "score": score,
              "max_length_word": max_length_word,
              "min_length_word": min_length_word,
              "average_token_length": average_token_length,
              "sorted_common": sorted_common}
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
    # Check for bad input
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profiles, list)
            or not isinstance(languages, list)
            or not isinstance(top_n, int)):
        return None
    # Generate reports on every eligible profile
    reports = []
    for profile in profiles:
        if profile["name"] in languages or not languages:
            report = compare_profiles_advanced(unknown_profile,
                                               profile,
                                               top_n)
            reports.append(report)
    # If no report is available, language input was bad
    if not reports:
        return None
    # Sort by score.
    reports = sorted(reports, key=lambda x: x["score"], reverse=True)
    # If the highest score appears in the list more than once,
    # The best-scoring reports need to be sorted alphabetically.
    best_scores = [report["score"] for report in reports]
    if best_scores.count(max(best_scores)) > 1:
        # Drop non-best-scoring reports
        reports = [report for report in reports
                   if report["score"] == max(best_scores)]
        # Sort alphabetically
        reports = sorted(reports, key=lambda x: x["name"])
    # Best fitting language
    language = reports[0]["name"]
    return language


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    # Check for bad input
    if (not isinstance(path_to_file, str)
            or not exists(path_to_file)):
        return None
    # Load profile from file
    with open(path_to_file, encoding="utf8") as file:
        profile = json.load(file)
    if profile:
        return profile
    return None


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    # Check for bad input
    if not isinstance(profile, dict):
        return 1
    if ("name" not in profile.keys()
            or "freq" not in profile.keys()
            or "n_words" not in profile.keys()):
        return 1
    if (not isinstance(profile["name"], str)
            or not isinstance(profile["freq"], dict)
            or not isinstance(profile["n_words"], int)):
        return 1
    # Generate file name from profile name
    path_to_file = "{}.json".format(profile["name"])
    # Save profile in json file
    with open(path_to_file, "w", encoding="utf8") as file:
        json.dump(profile, file)
    return 0
