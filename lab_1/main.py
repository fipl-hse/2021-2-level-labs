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
    if not isinstance(text, str):
        return None
    # split the text to low-case words
    words = text.lower().split()
    tokens = []
    # get the list of tokens: go through every word, through every symbol of the word.
    # If the symbol is not a letter, it's not added to the token
    for word in words:
        token = ''
        for i in range(len(word)):
            if word[i].isalpha():
                token += word[i]
            else:
                continue
        # if token has at least 1 letter after iteration through the word, it is added to the list of tokens
        if len(token):
            tokens.append(token)
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list):
        return None
    elif not isinstance(stop_words, list):
        return None
    # list comprehension: create the list of tokens without stop_words: iterate through tokens,
    # if the token is in the stop_words, it is not added to the list
    return [i for i in tokens if i not in stop_words]


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    freq_dict = {}
    # create frequency dictionary: iterate through tokens. If the token is not in the freq_dict kes,
    # it is added with value = 1, if it is in the list, the value increases by one
    for i in tokens:
        if i in freq_dict.keys() and isinstance(i, str):
            freq_dict[i] += 1
        elif i not in freq_dict.keys() and isinstance(i, str):
            freq_dict[i] = 1
        else:
            return None
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    top_words = []
    # sort frequency dictionary by values in reversed mode: words with the highest frequency go first
    top_freq = sorted(list(freq_dict.values()), reverse=True)
    # iterate through sorted dict, get the words with highest frequency, add them to the list
    for i in top_freq:
        for key in freq_dict.keys():
            if freq_dict[key] == i:
                top_words.append(key)
                freq_dict[key] = -1
    # return first top_n words with the highest frequency
    return top_words[:top_n]


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str) or not isinstance(text, str) or not isinstance(stop_words, list):
        return None
    # tokenize text, remove stop words
    tokens_processed = remove_stop_words(tokenize(text), stop_words)
    # create frequency dictionary
    frequency_dict = calculate_frequencies(tokens_processed)
    # get the number of words in the frequency dictionary
    num_of_words = len(frequency_dict)
    # return language profile
    return {"name": language,
            "freq": frequency_dict,
            "n_words": num_of_words}


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None
    # get top_n tokens from unknown language
    top_n_tokens_unknown_lang = get_top_n_words(unknown_profile["freq"], top_n)
    # get top_n tokens from known language
    top_n_tokens_compare_lang = get_top_n_words(profile_to_compare["freq"], top_n)
    # get the set of common tokens from both languages
    common_tokens = set.intersection(set(top_n_tokens_unknown_lang), set(top_n_tokens_compare_lang))
    # return compared profiles, distance
    return round(len(common_tokens) / len(top_n_tokens_unknown_lang), 2)


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
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) \
            or not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None
    # compare unknown profile to profile_1 and profile_2
    unknown_lang_to_profile_1 = compare_profiles(unknown_profile, profile_1, top_n)
    unknown_lang_to_profile_2 = compare_profiles(unknown_profile, profile_2, top_n)
    # return the detected language (if profiles are equal, return the 1st language in alphabetical order)
    if unknown_lang_to_profile_1 == unknown_lang_to_profile_2:
        return sorted([profile_1["name"], profile_2["name"]])[0]
    elif unknown_lang_to_profile_1 > unknown_lang_to_profile_2:
        return profile_1["name"]
    else:
        return profile_2["name"]


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
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None
    unknown_top_n_words = sorted(get_top_n_words(unknown_profile["freq"], top_n))
    to_compare_top_n_words = sorted(get_top_n_words(profile_to_compare["freq"], top_n))

    # find 'common'
    common = [i for i in to_compare_top_n_words if i in unknown_top_n_words]

    # find 'sorted common'
    sorted_common = sorted(common)

    # find 'score'
    score = len(common) / len(unknown_top_n_words)

    # find 'max_length_word'
    list_of_words = sorted(list(profile_to_compare["freq"].keys()), key=len)
    max_length_word = list_of_words[-1]

    # find 'min_length_word'
    min_length_word = list_of_words[0]

    # find 'average_token_length'
    total_len = 0
    for i in list_of_words:
        total_len += len(i)
    average_token_length = total_len / len(list_of_words)

    record = {'name': profile_to_compare["name"],
              'common': common,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted_common}
    return record


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
    if not isinstance(unknown_profile, dict) or not isinstance(profiles, list) \
            or not isinstance(languages, list) or not isinstance(top_n, int):
        return None
    # find all records
    all_records = []
    for known_profile in profiles:
        record = compare_profiles_advanced(unknown_profile, known_profile, top_n)
        if languages:
            if known_profile["name"] in languages:
                all_records.append(record)
            else:
                continue
        else:
            all_records.append(record)
    if not all_records:
        return None
    # find the record with maximum score and get it's language
    all_scores = []
    for record in all_records:
        all_scores.append(record["score"])
    max_score = sorted(all_scores)[-1]
    detected_languages = []
    for i in all_records:
        if i['score'] == max_score:
            detected_languages.append(i['name'])
    return sorted(detected_languages)[0]


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str) or not exists(path_to_file):
        return None
    # open json file for reading
    my_file = open(path_to_file, "r", encoding="utf-8")
    # convert to dict
    profile = json.load(my_file)
    # close file
    my_file.close()
    # return dictionary
    return profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict) or ("n_words" or "name" or "freq") not in profile.keys():
        return 1
    if not isinstance(profile["name"], str) or not isinstance(profile["freq"], dict) or\
            not isinstance(profile["n_words"], int):
        return 1
    # create path/name of the file
    my_path = f'{profile["name"]}.json'
    # open the file for writing
    my_file = open(my_path, "w", encoding="utf-8")
    # save profile to json file
    json.dump(profile, my_file)
    # close file
    my_file.close()
    return 0
