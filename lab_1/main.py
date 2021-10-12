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
<<<<<<< HEAD
#<<<<<<< HEAD
    tokens = ''
    for i in text:
        if i.isalpha() or i.isspace():
            tokens += i

    tokens = tokens.lower().split()
#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    invaluable_trash = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                        '.', '?', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    text = text.lower()
    for symbols in invaluable_trash:
        text = text.replace(symbols, '')
    tokens = text.split()
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    if not (isinstance(stop_words, list) and isinstance(tokens, list)):
        return None
    tokens_new = []
    for i in tokens:
        if i not in stop_words:
            tokens_new.append(i)
    return tokens_new
#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    new_tokens = []
    for word in tokens:
        if word not in stop_words:
            new_tokens.append(word)
    return new_tokens
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
<<<<<<< HEAD
<<<<<<< HEAD
   Calculates frequencies of given tokens
   :param tokens: a list of tokens
   :return: a dictionary with frequencies
   """
    if not (isinstance(tokens_new, list) and isinstance(tokens_new[0], str)):
        return None
    freq_dict = {}
    for i in tokens_new:
        if i not in freq_dict:
            freq_dict[i] = 1
        else:
            freq_dict[i] += 1
    return freq_dict

#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    if not isinstance(tokens, list):
        return None
    frequency_dictionary = {}
    for word in tokens:
        if isinstance(word, str):
            if word in frequency_dictionary:
                frequency_dictionary[word] += 1
            else:
                frequency_dictionary[word] = 1
        else:
            return None
    return frequency_dictionary
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    if not (isinstance(freq_dict, dict) and isinstance(top_n, int)):
        return None
    if top_n <= 0:
        return []
    top_n_words = []
    if top_n > len(freq_dict):
        top_n = len(freq_dict)
    freq_dict_copy = freq_dict.copy()
    top_n_copy = top_n
    while top_n_copy != 0:
        max_value = max(freq_dict_copy.values())
        for key, value in freq_dict_copy.items():
            if value == max_value:
                max_key = key
                break
        top_n_words.append(max_key)
        del freq_dict_copy[max_key]
        top_n_copy -= 1
    return top_n_words
#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    # sort by keys and take the top_n tokens from the list of sorted tokens
    top_n_words = sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]
    return top_n_words

<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7

def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    freq_dict = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
    if not (isinstance(language, str) and isinstance(freq_dict, dict)):
        return None
    language_profile = {'name': language,
                        'freq': freq_dict,
                        'n_words': len(freq_dict)}
    return language_profile
#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
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
    # create and return language profile
    return {"name": language, "freq": frequency_dictionary, "n_words": n_words}
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    top_n_words_profile_to_compare = get_top_n_words(profile_to_compare['freq'], top_n)
    common = []
    for i in top_n_words_unknown_profile:
        if i in top_n_words_profile_to_compare:
            common.append(i)
    return round(len(common) / len(top_n_words_unknown_profile), 2)

'''
def detect_language(unknown_profile: dict, profile_1: dict,
#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
    # use function get_top_n_words
    top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    # find common tokens WITHOUT creating list
    common_things = set(top_n_words_unknown) & set(top_n_words_compare)
    # find share of common tokens
    share_of_common_things = round(len(common_things)/len(top_n_words_unknown), 2)
    return share_of_common_things
'''

def detect_language(unknown_profile: dict,
                    profile_1: dict,
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
                    profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    percentage_1 = compare_profiles(unknown_profile, profile_1, top_n)
    percentage_2 = compare_profiles(unknown_profile, profile_2, top_n)
    if not (isinstance(percentage_1, float) and isinstance(percentage_2, float)):
        return None
    if percentage_1 > percentage_2:
        return profile_1['name']
    if percentage_1 < percentage_2:
        return profile_2['name']
    return [profile_1['name'], profile_2['name']].sort()[0]


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict,
                              top_n: int) -> list or None:
#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
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
        language_name = sorted([profile_1["name"], profile_2["name"]])[0]
    elif share_the_first_language > share_the_second_language:
        language_name = profile_1["name"]
    else:
        language_name = profile_2["name"]
    return language_name


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> dict or None:
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    top_n_words_profile_to_compare = get_top_n_words(profile_to_compare['freq'], top_n)
    common = []
    for i in top_n_words_profile_to_compare:
        if i in top_n_words_unknown_profile:
            common.append(i)
    score = len(common) / len(top_n_words_unknown_profile)
    sorted_common = sorted(common)
    sorted_tokens = sorted(list(profile_to_compare['freq'].keys()), key=len)
    min_length_word = sorted_tokens[0]
    max_length_word = sorted_tokens[-1]
    common_length = 0
    for i in sorted_tokens:
        common_length += len(i)
    average_token_length = common_length/len(sorted_tokens)
    report = {'name': profile_to_compare['name'], 'common': common, 'score': score,
              'max_length_word': max_length_word, 'min_length_word': min_length_word,
              'average_token_length': average_token_length, 'sorted_common': sorted_common}
    return report

def detect_language_advanced(unknown_profile: dict, profiles: list,
                             languages: list, top_n: int) -> str or None:
#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
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
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    if not(isinstance(unknown_profile, dict) and isinstance(profiles, list)
           and isinstance(languages, list) and isinstance(top_n, int)):
        return None
    reports = []
    for current_profile in profiles:
        if current_profile['name'] in languages or not languages:
            reports.append(compare_profiles_advanced(unknown_profile, current_profile, top_n))
    if not reports:
        return None
    reports = sorted(reports, key=lambda k: k['score'], reverse=True)
    # to put languages in alphabetical score if there are some similar scores
    counter = 0
    for i in range(len(reports)-1):
        if reports[i]['score'] == reports[i+1]['score']:
            counter += 1
        else:
            break
    if counter != 0:
        language = sorted([reports[i]['name'] for i in range(0, counter+1)])[0]
    else:
        language = reports[0]['name']
    return language
#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profiles, list)
            or not isinstance(languages, list)
            or not isinstance(top_n, int)):
        return None
    # create the list of reports (they are dict) and sort the reports by score
    reports = []
    for profile in profiles:
        if profile["name"] in languages or not languages:
            report = compare_profiles_advanced(unknown_profile, profile, top_n)
            reports.append(report)
    reports = sorted(reports, key=lambda x: x["score"], reverse=True)
    if not reports:
        return None
    # sort in alphabetically order if some languages have the same max scores
    # create the list with only scores and count the max score-element in it
    list_with_only_scores = []
    for element_dict in reports:
        list_with_only_scores.append(element_dict["score"])
    max_scores = max(list_with_only_scores)
    number_of_max_scores = list_with_only_scores.count(max_scores)
    # use the count as a stop index to take the part of the 'reports' that we want to sort
    reports = sorted(reports[:number_of_max_scores], key=lambda x: x["name"])
    # return a language
    return reports[0]["name"]

<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7

def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    if not isinstance(path_to_file, str) or not exists(path_to_file):
        return None
    with open(path_to_file, encoding='utf-8') as file:
        profile = json.load(file)
    if profile:
        return profile
    return None

#=======
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
    # check for bad input
    if not isinstance(path_to_file, str) or not exists(path_to_file):
        return None
    # load profile from file
    with open(path_to_file, "r", encoding="utf-8") as json_file:
        profile = json.load(json_file)
    return profile
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
<<<<<<< HEAD
#<<<<<<< HEAD
    if not isinstance(profile, dict) or ('name' or 'freq' or 'n_words') not in profile.keys():
        return 1
    if not (isinstance(profile['name'], str) and isinstance(profile['freq'], dict)
            and isinstance(profile['n_words'], int)):
=======
    if not isinstance(profile, dict) or ("name" or "freq" or "n_words") not in profile.keys():
        return 1
    if (not isinstance(profile["name"], str)
            or not isinstance(profile["freq"], dict)
            or not isinstance(profile["n_words"], int)):
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
        return 1
    # generate file name from profile name
    path_to_file = "{}.json".format(profile["name"])
    # save profile in json file
    with open(path_to_file, "w", encoding="utf-8") as file:
<<<<<<< HEAD
#>>>>>>> upstream/main
=======
>>>>>>> f879af63c19cd3ab83fafc164775077f80f0bfd7
        json.dump(profile, file)
    return 0
