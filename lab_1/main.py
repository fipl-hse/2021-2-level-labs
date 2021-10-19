"""
Lab 1
Language detection
"""
import json
from os.path import exists
import re


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
#     invaluable_trash = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
#                         '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
#                         '.', '?', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
#     text = text.lower()
# <<<<<<< HEAD
    text = re.sub('[^a-züöäß \n]', '', text)    # ищем небуквенные символы
    # ищет подстроку по шаблону и заменяет ее на пробел; пропускает перенос строки
    text = text.split()
    return text


# def remove_stop_words(tokens: list,
#                       stop_words: list) -> list or None:
# # =======
#     for symbols in invaluable_trash:
#         text = text.replace(symbols, '')
#     tokens = text.split()
#     return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
# >>>>>>> 94359393a8b8a88ab306da1febf438dd20af6781
=======
    invaluable_trash = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                        '.', '?', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    text = text.lower()
    for symbols in invaluable_trash:
        text = text.replace(symbols, '')
    tokens = text.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
>>>>>>> 9ad88167d204ed092ff0d3c999b85a4ea4ccbdfe
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
<<<<<<< HEAD
# <<<<<<< HEAD
    tokens = [n for n in tokens if n not in stop_words]
    return tokens

# =======
#     new_tokens = []
#     for word in tokens:
#         if word not in stop_words:
#             new_tokens.append(word)
#     return new_tokens
# >>>>>>> 94359393a8b8a88ab306da1febf438dd20af6781
=======
    new_tokens = []
    for word in tokens:
        if word not in stop_words:
            new_tokens.append(word)
    return new_tokens

>>>>>>> 9ad88167d204ed092ff0d3c999b85a4ea4ccbdfe

def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
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


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
<<<<<<< HEAD
# <<<<<<< HEAD
    sorted_most_common = dict(sorted(freq_dict.items(), key=lambda x: -x[1]))
    # key - уточняет по какому критерию идет сортировка,
    # х - элемент, х[1] - частота этого элемента(токена); для того чтобы сортировка шла по убыванию ставим "-"
    # Лямбда принимает любое количество аргументов (или ни одного) и состоит из одного выражения.
    common_words = list(sorted_most_common)
    common_words = common_words[:top_n]
    return common_words
# =======
#     # sort by keys and take the top_n tokens from the list of sorted tokens
#     top_n_words = sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]
#     return top_n_words
# >>>>>>> 94359393a8b8a88ab306da1febf438dd20af6781
=======
    # sort by keys and take the top_n tokens from the list of sorted tokens
    top_n_words = sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]
    return top_n_words
>>>>>>> 9ad88167d204ed092ff0d3c999b85a4ea4ccbdfe


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
    # create and return language profile
    return {"name": language, "freq": frequency_dictionary, "n_words": n_words}


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
<<<<<<< HEAD
# <<<<<<< HEAD
    profile_compared = profile_to_compare['freq']
    profile_compared_top = get_top_n_words(profile_compared, top_n)
    unknown_profile_needed = unknown_profile['freq']
    unknown_profile_top = get_top_n_words(unknown_profile_needed, top_n)
    common_tokens = 0
    for i in unknown_profile_top:
        if i in profile_compared_top:
            common_tokens += 1
    distance = round(common_tokens/(len(unknown_profile_top)), 2)  # доля пересекающихся частотных слов.
    return distance
# =======
#     # use function get_top_n_words
#     top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
#     top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
#     # find common tokens WITHOUT creating list
#     common_things = set(top_n_words_unknown) & set(top_n_words_compare)
#     # find share of common tokens
#     share_of_common_things = round(len(common_things)/len(top_n_words_unknown), 2)
#     return share_of_common_things
# >>>>>>> 94359393a8b8a88ab306da1febf438dd20af6781
=======
    # use function get_top_n_words
    top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    # find common tokens WITHOUT creating list
    common_things = set(top_n_words_unknown) & set(top_n_words_compare)
    # find share of common tokens
    share_of_common_things = round(len(common_things)/len(top_n_words_unknown), 2)
    return share_of_common_things
>>>>>>> 9ad88167d204ed092ff0d3c999b85a4ea4ccbdfe


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
        language_name = sorted([profile_1["name"], profile_2["name"]])[0]
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
<<<<<<< HEAD
# <<<<<<< HEAD
    profile_compared_top1 = get_top_n_words(profile_to_compare['freq'], top_n)
    unknown_profile_top = get_top_n_words(unknown_profile['freq'], top_n)
    most_common_words1 = []
    for i in profile_compared_top1:
        if i in unknown_profile_top:
            most_common_words1.append(i)
    common_score = len(most_common_words1)/len(unknown_profile_top)  # доля пересекающихся частотных слов.
    words = list(profile_to_compare['freq'].keys())
    max_length = max(words, key=len)
    min_length = min(words, key=len)
    length_word = 0
    for i, word in enumerate(words):  # enumerate() позволяет перебирать элементов, отслеживая индекс текущего элемента.
        if word in words:
            length_word += len(words[i])
    average_length = length_word / len(words)
    comp_prof_adv = {'name': profile_to_compare['name'],
                     'score': common_score,
                     'common': most_common_words1,
                     'sorted_common': sorted(most_common_words1),
                     'max_length_word': max_length,
                     'min_length_word': min_length,
                     'average_token_length': average_length}
    return comp_prof_adv
# # =======
#     # use function get_top_n_words to get common and sorted_common
#     top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
#     top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
#     common = []
#     for word in top_n_words_compare:
#         if word in top_n_words_unknown:
#             common.append(word)
#     sorted_common = sorted(common)
#     # get score
#     score = round(len(common) / len(top_n_words_unknown), 2)
#     # get max and min length of words
#     max_length_word = max(profile_to_compare["freq"].keys(), key=len)
#     min_length_word = min(profile_to_compare["freq"].keys(), key=len)
#     # get average_token_length via list with length of tokens
#     length_of_tokens = []
#     for token in profile_to_compare["freq"].keys():
#         length_of_tokens.append(len(token))
#     average_token_length = sum(length_of_tokens)/len(profile_to_compare["freq"].keys())
#     # get a report
#     report = {'name': profile_to_compare["name"],
#               'common': common,
#               'score': score,
#               'max_length_word': max_length_word,
#               'min_length_word': min_length_word,
#               'average_token_length': average_token_length,
#               'sorted_common': sorted_common}
#     return report
# >>>>>>> 94359393a8b8a88ab306da1febf438dd20af6781
=======
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
>>>>>>> 9ad88167d204ed092ff0d3c999b85a4ea4ccbdfe


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
    # create the list of reports (they are dict) and sort the reports by score
    reports = []
    for profile in profiles:
        if profile["name"] in languages or not languages:
            report = compare_profiles_advanced(unknown_profile, profile, top_n)
            reports.append(report)
    reports = sorted(reports, key=lambda x: x["score"], reverse=True)
    if not reports:
        return None
<<<<<<< HEAD
# # <<<<<<< HEAD
#     max_score = [max(score)]
#     result_score = {}
#     keys = dict_score.keys()
#     for k in keys:
#         for i in max_score:
#             if dict_score[k] == i:
#                 result_score[k] = i
#     result = list(sorted(result_score.keys()))
#     return result[0]


# def load_profile(path_to_file: str) -> dict or None:
#     """
#     Loads a language profile
#     :param path_to_file: a path
#     :return: a dictionary with three keys – name, freq, n_words
#     """
#     pass
#
#
# def save_profile(profile: dict) -> int:
#     """
#     Saves a language profile
#     :param profile: a dictionary
#     :return: 0 if everything is ok, 1 if not
#     """
#     pass

#need
# =======
#     # sort in alphabetically order if some languages have the same max scores
#     # create the list with only scores and count the max score-element in it
#     list_with_only_scores = []
#     for element_dict in reports:
#         list_with_only_scores.append(element_dict["score"])
#     max_scores = max(list_with_only_scores)
#     number_of_max_scores = list_with_only_scores.count(max_scores)
#     # use the count as a stop index to take the part of the 'reports' that we want to sort
#     reports = sorted(reports[:number_of_max_scores], key=lambda x: x["name"])
#     # return a language
#     return reports[0]["name"]
=======
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
>>>>>>> 9ad88167d204ed092ff0d3c999b85a4ea4ccbdfe


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    # check for bad input
    if not isinstance(path_to_file, str) or not exists(path_to_file):
        return None
    # load profile from file
    with open(path_to_file, "r", encoding="utf-8") as json_file:
        profile = json.load(json_file)
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
<<<<<<< HEAD
# >>>>>>> 94359393a8b8a88ab306da1febf438dd20af6781
=======
>>>>>>> 9ad88167d204ed092ff0d3c999b85a4ea4ccbdfe
