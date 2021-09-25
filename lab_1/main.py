"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

    word = []
    tokens = []
    if isinstance(text, str):
        text = text.lower()
        for i in text:
            if i.isalpha():
                word.append(i)
            elif i.isspace():
                if word:
                    tokens.append(''.join(word))
                word = []
        if len(word) > 0:
            tokens.append(''.join(word))
        return tokens
    else:
        return None


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if isinstance(tokens, list):
        for i in tokens:
            if isinstance(i, str):
                tokens = [i for i in tokens if i not in stop_words]
                return tokens
    else:
        return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    freq_dict = {}
    if isinstance(tokens, list):
        for i in tokens:
            if isinstance(i, str):
                for _ in tokens:
                    if _ in freq_dict:
                        freq_dict[_] += 1
                    else:
                        freq_dict[_] = 1
                return freq_dict
    else:
        return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    top_words = []
    if isinstance(freq_dict, dict):
        if all(isinstance(e, str) for e in list(freq_dict.keys())):
            top_words = sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]
        return top_words
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
        freq_dict = calculate_frequencies(tokens)
        n_words = len(freq_dict)
        language_profile = dict(name=language, freq=freq_dict, n_words=n_words)
        return language_profile
    else:
        return None


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    common = []
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) \
            and isinstance(top_n, int):
        unknown = get_top_n_words(unknown_profile.get('freq'), top_n)
        compare = get_top_n_words(profile_to_compare.get('freq'), top_n)
        for i in unknown:
            if i in compare:
                common.append(i)
        distance = round(len(common) / len(unknown), 2)
        return distance
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

    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) \
            and isinstance(profile_2, dict) and isinstance(top_n, int):
        first = compare_profiles(unknown_profile, profile_1, top_n)
        second = compare_profiles(unknown_profile, profile_2, top_n)
        if first > second:
            return profile_1.get('name')
        elif first < second:
            return profile_2.get('name')
        else:
            return sorted([profile_1.get('name'), profile_2.get('name')])[0]
    else:
        return None


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """

    common = []
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) \
            and isinstance(top_n, int):
        tokens = list(profile_to_compare.get('freq').keys())
        max_length_word = max(tokens, key=len)
        min_length_word = min(tokens, key=len)
        unknown = get_top_n_words(unknown_profile.get('freq'), top_n)
        compare = get_top_n_words(profile_to_compare.get('freq'), top_n)
        for i in compare:
            if i in unknown:
                common.append(i)
        score = len(common) / len(compare)
        whole_len = 0
        for i in tokens:
            whole_len += len(i)
        average_token_length = whole_len / len(tokens)
        sorted_common = sorted(common)
        language_profile = {'name': profile_to_compare.get('name'),
                            'common': common,
                            'score': score,
                            'max_length_word': max_length_word,
                            'min_length_word': min_length_word,
                            'sorted_common': sorted_common,
                            'average_token_length': average_token_length}
        return language_profile
    else:
        return None

def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """

    score = {}
    if isinstance(unknown_profile, dict) and isinstance(profiles, list) \
            and isinstance(languages, list) and isinstance(top_n, int):
        exist_lang = False
        for _ in profiles:
            if languages:
                for i in languages:
                    if i == _.get('name'):
                        exist_lang = True
                        score[i] = compare_profiles_advanced(unknown_profile, _, top_n).get('score')
            else:
                score[_.get('name')] = compare_profiles_advanced(unknown_profile, _, top_n).get('score')
        if not exist_lang and languages:
            return None
        sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)
        i = 0
        first_score = sorted_score[0][1]
        name_list = []
        while i < len(sorted_score) and first_score == sorted_score[i][1]:
            name_list.append(sorted_score[i][0])
            i += 1
        name_list_sorted = sorted(name_list)
        return name_list_sorted[0]
    else:
        return None


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
