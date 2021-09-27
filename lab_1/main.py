"""
Lab 1
Language detection
"""
import re
def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if isinstance(text, str):
        text = text.lower()
        text = re.sub('[^a-züöäß \n]', '', text)
        text = text.split()
        return text
    return None


def remove_stop_words(tokens: list,
                      stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if (isinstance(tokens, list)
            and isinstance(stop_words, list)):
        if tokens:
            tokens = [n for n in tokens if n not in stop_words]
            return tokens
    return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if isinstance(tokens, list):
        freq_dict = {}
        for word in tokens:
            if not isinstance(word, str):
                return None
            if word not in freq_dict:
                freq_dict[word] = 1
            else:
                freq_dict[word] += 1
        return freq_dict
    return None

def get_top_n_words(freq_dict: dict,
                    top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if isinstance(freq_dict, dict):
        sorted_most_common = dict(sorted(freq_dict.items(), key=lambda x: -x[1]))
        common_words = list(sorted_most_common)
        common_words = common_words[:top_n]
        return common_words
    return None

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
    if (isinstance(language, str)
            and isinstance(text, str)
            and isinstance(stop_words, list)):
        tokens = tokenize(text)
        tokens = remove_stop_words(tokens, stop_words)
        freq_dict = calculate_frequencies(tokens)
        language_dict = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
        return language_dict
    return None

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
    if (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        profile_compared = profile_to_compare['freq']
        profile_compared_top = get_top_n_words(profile_compared, top_n)
        unknown_profile_needed = unknown_profile['freq']
        unknown_profile_top = get_top_n_words(unknown_profile_needed, top_n)
        common_tokens = 0
        for i in unknown_profile_top:
            if i in profile_compared_top:
                common_tokens += 1
        distance = round(common_tokens/(len(profile_compared_top)), 2)
        return distance
    return None

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
    if (isinstance(unknown_profile, dict)
            and isinstance(profile_1, dict)
            and isinstance(profile_2, dict)
            and isinstance(top_n, int)):
        unknown = unknown_profile['freq']
        unknown_needed = get_top_n_words(unknown, top_n)
        profile_compare_1 = profile_1['freq']
        prof_comp_1 = get_top_n_words(profile_compare_1, top_n)
        profile_compare_2 = profile_2['freq']
        prof_comp_2 = get_top_n_words(profile_compare_2, top_n)
        for i in unknown_needed:
            if i in prof_comp_1:
                i = profile_1['name']
            elif i in prof_comp_2:
                i = profile_2['name']
            return i
    return None

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
    if (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        profile_compared_top1 = get_top_n_words(profile_to_compare['freq'], top_n)
        unknown_profile_top = get_top_n_words(unknown_profile['freq'], top_n)
        most_common_words1 = []
        for i in profile_compared_top1:
            if i in unknown_profile_top:
                most_common_words1.append(i)
        common_score = len(most_common_words1)/len(unknown_profile_top)
        words = list(profile_to_compare['freq'].keys())
        max_length = max(words, key=len)
        min_length = min(words, key=len)
        length_word = 0
        for i, word in enumerate(words):
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
    return None

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
    if (isinstance(unknown_profile, dict)
            and isinstance(profiles, list)
            and (languages, list)
            and (top_n, int)):
        dict_score = {}
        for profile in profiles:
            if len(languages) == 0 or profile['name'] in languages:
                profile_unk = compare_profiles_advanced(unknown_profile, profile, top_n)
                dict_score[profile['name']] = profile_unk['score']
        score = list(dict_score.values())
        if len(score) == 0:
            return None
        max_score = [max(score)]
        result_score = {}
        keys = dict_score.keys()
        for k in keys:
            for i in max_score:
                if dict_score[k] == i:
                    result_score[k] = i
        result = list(sorted(result_score.keys()))
        return result[0]
    return None

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
