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
        skip_signs = ["'", "-", "%", ">", "<", "$", "@", "#", "&", "*"]
        for g in text:
            if g in skip_signs:
                text = text.replace(g, "")
        text = re.sub(r'[^\w\s]', '', text)  # delete punctuation
        text = re.sub(r"\d+", "", text)  # delete numbers
        tokens = re.split("\s", text)
        for q in tokens:
            if q == '':
                tokens.remove(q)
        return tokens
    else:
        return None


def remove_stop_words(tokens: list, stop_words: list):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words.words(language): a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(tokens, list) and isinstance(stop_words, list):
        if tokens:
            for j in range(len(tokens)):
                if tokens[j] in stop_words:
                    tokens[j] = ''

            while '' in tokens:
                tokens.remove('')
            return tokens
        else:
            return None
    else:
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
            else:
                return None
    else:
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
    else:
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
    else:
        return None

    pass


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        profile_to_compare_tokens = get_top_n_words(profile_to_compare['freq'], top_n)
        unknown_profile_tokens = get_top_n_words(unknown_profile['freq'], top_n)
        shared_tokens = 0
        for i in unknown_profile_tokens:
            if i in profile_to_compare_tokens:
                shared_tokens += 1
        common_freq_words = shared_tokens / len(profile_to_compare_tokens)
        common_freq_words = round(common_freq_words, 2)
        return common_freq_words
    else:
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
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) and isinstance(profile_2, dict) and isinstance(
            top_n, int):
        profile_1_words = compare_profiles(unknown_profile, profile_1, top_n)
        profile_2_words = compare_profiles(unknown_profile, profile_2, top_n)
        name1 = profile_1['name']
        name2 = profile_2['name']
        if profile_1_words > profile_2_words:
            return name1
        elif profile_2_words > profile_1_words:
            return name2
        elif profile_2_words == profile_1_words:
            names = [name1, name2]
            names.sort()
            return names[0]


    else:
        return None


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        unk_top_words = get_top_n_words(unknown_profile['freq'], top_n)
        comp_top_words = get_top_n_words(profile_to_compare['freq'], top_n)
        shared_tokens = []
        for i in range(len(comp_top_words)):
            if comp_top_words[i] in unk_top_words:
                shared_tokens.append(comp_top_words[i])
        score = compare_profiles(unknown_profile,profile_to_compare, top_n)
        words = list(profile_to_compare['freq'].keys())
        print(words)
        max_length_word = 'a'
        for i in range(len(words)):
            if len(words[i]) > len(max_length_word):
                max_length_word = words[i]
        min_length_word = 100 * 'a'
        for i in range(len(words)):
            if len(words[i]) < len(min_length_word):
                min_length_word = words[i]
        sum_letters = 0
        for i in range(len(words)):
            sum_letters += len(words[i])
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
    else:
        return None
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    if isinstance(unknown_profile,dict) and isinstance(profiles, list) and isinstance(languages, list) and isinstance(top_n, int):
        if not languages:
            profiles_words = {}
            for i in range(len(profiles)):
                number = compare_profiles(unknown_profile, profiles[i], top_n)
                name = profiles[i]['name']
                profiles_words[name] = number
            list_of_keys = list(profiles_words.keys())
            if len(profiles) == 1:
                name_for_1 = profiles[0]['name']
                return name_for_1
            if profiles_words[list_of_keys[0]] > profiles_words[list_of_keys[1]]:
                return list_of_keys[0]
            elif profiles_words[list_of_keys[0]] < profiles_words[list_of_keys[1]]:
                return list_of_keys[1]
            elif profiles_words[list_of_keys[0]] == profiles_words[list_of_keys[1]]:
                names = [list_of_keys[0], list_of_keys[1]]
                names.sort()
                return names[0]
        else:
            true_profiles = []
            for i in range(len(profiles)):
                if profiles[i]['name'] in languages:
                    true_profiles.append(profiles[i])
            if true_profiles == []:
                return None
            if len(true_profiles) == 1:
                name_for_1 = profiles[0]['name']
                return name_for_1
            profiles_words = {}
            for i in range(len(true_profiles)):
                number = compare_profiles(unknown_profile, true_profiles[i], top_n)
                name = true_profiles[i]['name']
                profiles_words[name] = number
            list_of_keys = list(profiles_words.keys())
            if len(true_profiles) == 1:
                return true_profiles[0]
            if profiles_words[list_of_keys[0]] > profiles_words[list_of_keys[1]]:
                return list_of_keys[0]
            elif profiles_words[list_of_keys[0]] < profiles_words[list_of_keys[1]]:
                return list_of_keys[1]
            elif profiles_words[list_of_keys[0]] == profiles_words[list_of_keys[1]]:
                names = [list_of_keys[0], list_of_keys[1]]
                names.sort()
                return names[0]


    else:
        return None
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
    if isinstance(path_to_file,str):
        try:
            with open(path_to_file, 'r', encoding='utf-8') as f:
                text = json.load(f)
            return text
        except FileNotFoundError:
            return None
    else:
        return None
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """


def save_profile(profile: dict) -> int:
    if isinstance(profile,dict):
        json.dumps(profile,profile['name'])
        return 0
    else:
        return 1
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
