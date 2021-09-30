"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    if isinstance(text, str):
        textnew = ''
        for i in text:
            i = i.lower()
            if i.isalpha() or i.isspace():
                textnew = textnew + i
        tokens = textnew.split()
        return tokens
    else:
        return None


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    if isinstance(tokens, list) and len(tokens) != 0:
        new_tokens = []
        for i in tokens:
            if i in stop_words:
                continue
            else:
                new_tokens.append(i)
        return new_tokens
    else:
        return None


def calculate_frequencies(tokens: list) -> dict or None:
    k = 0
    if isinstance(tokens, list) and len(tokens) != 0:
        for i in tokens:
            if i == None:
                k = 1
                break
        if k == 1:
            return None
        else:
            freq_list = {}
            for i in tokens:
                if i in freq_list.keys():
                    freq_list[i] += 1
                else:
                    freq_list[i] = 1
            return freq_list
    else:
        return None

def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    if isinstance(freq_dict, dict):
        keys = []
        for i in freq_dict.keys():
            keys.append(i)
        nums = []
        new_keys = []
        for i in freq_dict:
            nums.append(freq_dict.get(i))
        for i in range(len(nums)-1):
            for j in range(i,len(nums)):
                if nums[i]<nums[j]:
                    n=nums[i]
                    nums[i]=nums[j]
                    nums[j]=n

                    k=keys[i]
                    keys[i] = keys[j]
                    keys[j] = k
        if top_n> len(keys):
            return keys
        else:
            for i in range(top_n):
                new_keys.append(keys[i])
            return new_keys
    return None


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
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
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
