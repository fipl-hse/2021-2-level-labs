"""
Lab 1
Language detection
"""
import re
import json


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if isinstance(text, str):
        text = text.lower()
        skip_signs = ["'", "-", "%", ">", "<", "$", "@", "#", "&", "*", ",", ".", "!", ":", "º"]
        for element in text:
            if element in skip_signs:
                text = text.replace(element, "")
        text = re.sub(r"\d+", "", text)  # delete numbers
        tokens = re.split(r"\s", text)
        for token in tokens:
            if token == '':
                tokens.remove(token)
        return tokens
    return None


def remove_stop_words(tokens: list, stop_words: list):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(tokens, list) and isinstance(stop_words, list):
        if tokens:
            for token in enumerate(tokens):
                if token[1] in stop_words:
                    tokens[token[0]] = ''
            while '' in tokens:
                tokens.remove('')
            return tokens
        return None
    return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if isinstance(tokens, list):
        for j in tokens:
            if isinstance(j, str):
                freq_dict = {}
                for i in tokens:
                    if i in freq_dict:
                        freq_dict[i] += 1
                    else:
                        freq_dict[i] = 1
                return freq_dict
            return None
    return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if isinstance(freq_dict, dict):
        sorted_dict = dict(sorted(freq_dict.items(), reverse=True, key=lambda x: x[1]))
        most_comm_words = list(sorted_dict)
        most_comm_words = most_comm_words[:top_n]
        return most_comm_words
    return None


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        tokens = tokenize(text)
        tokens = remove_stop_words(tokens, stop_words)
        freq_dic = calculate_frequencies(tokens)
        ling_dict = {'name': language, 'freq': freq_dic, 'n_words': len(freq_dic)}
        return ling_dict
    return None


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) \
            and isinstance(top_n, int):
        profile_to_compare_tokens = get_top_n_words(profile_to_compare['freq'], top_n)
        unknown_profile_tokens = get_top_n_words(unknown_profile['freq'], top_n)
        shared_tokens = 0
        for i in unknown_profile_tokens:
            if i in profile_to_compare_tokens:
                shared_tokens += 1
        common_freq_words = shared_tokens / len(profile_to_compare_tokens)
        common_freq_words = round(common_freq_words, 2)
        return common_freq_words
    return None


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict,
                    top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) \
            and isinstance(profile_2, dict) and isinstance(
            top_n, int):
        profile_1_words = compare_profiles(unknown_profile, profile_1, top_n)
        profile_2_words = compare_profiles(unknown_profile, profile_2, top_n)
        name1 = profile_1['name']
        name2 = profile_2['name']
        if profile_1_words > profile_2_words:
            return name1
        if profile_2_words > profile_1_words:
            return name2
        if profile_2_words == profile_1_words:
            names = [name1, name2]
            names.sort()
            return names[0]
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
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) \
            and isinstance(top_n, int):
        unk_top_words = get_top_n_words(unknown_profile['freq'], top_n)
        comp_top_words = get_top_n_words(profile_to_compare['freq'], top_n)
        shared_tokens = []
        for comp_top_word in enumerate(comp_top_words):
            if comp_top_word[1] in unk_top_words:
                shared_tokens.append(comp_top_word[1])
        score = compare_profiles(unknown_profile, profile_to_compare, top_n)
        words = list(profile_to_compare['freq'].keys())
        max_length_word = 'a'
        for word_for_max in enumerate(words):
            if len(word_for_max[1]) > len(max_length_word):
                max_length_word = word_for_max[1]
        min_length_word = 100 * 'a'
        for word_for_min in enumerate(words):
            if len(word_for_min[1]) < len(min_length_word):
                min_length_word = word_for_min[1]
        sum_letters = 0
        for word_for_sum in enumerate(words):
            sum_letters += len(word_for_sum[1])
        average_token_length = sum_letters / len(words)
        sorted_common = shared_tokens.copy()
        sorted_common.sort()
        report = {'name': profile_to_compare['name'],
                  'common': shared_tokens,
                  'score': score,
                  'max_length_word': max_length_word,
                  'min_length_word': min_length_word,
                  'average_token_length': average_token_length,
                  'sorted_common': sorted_common}
        return report
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
    if isinstance(unknown_profile, dict) and isinstance(profiles, list) \
            and isinstance(languages, list) and \
            isinstance(top_n, int):
        list_of_languages = []
        for profile in profiles:
            if profile['name'] in languages or languages == []:
                compared_profile = compare_profiles_advanced(unknown_profile, profile, top_n)
                list_of_languages.append(compared_profile)
        list_of_languages = sorted(list_of_languages, reverse=True, key=lambda x: x['score'])
        if not list_of_languages:
            return None
        if len(list_of_languages) > 1:
            if list_of_languages[0]['score'] == list_of_languages[1]['score']:
                equal_scores = []
                for i in list_of_languages:
                    if i['score'] == list_of_languages[0]:
                        equal_scores.append(i)
                list_of_languages = sorted(equal_scores, reverse=True, key=lambda x: x['score'])
        return list_of_languages[0]['name']
    return None


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(path_to_file, str):
        try:
            with open(path_to_file, 'r', encoding='utf-8') as file:
                text = json.load(file)
            return text
        except FileNotFoundError:
            return None
    return None


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if isinstance(profile, dict):
        with open("{}.json".format(profile["name"]), 'w', encoding='utf-8') as file:
            json.dump(profile, file)
        return 0
    return 1
