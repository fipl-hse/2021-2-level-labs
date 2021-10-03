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
    if not isinstance(text, str):
        return None
    else:
        textnew = ''
        for i in text:
            i = i.lower()
            if i.isalpha() or i.isspace():
                textnew = textnew + i
        tokens = textnew.split()
        return tokens



def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
        Removes stop words
        :param tokens: a list of tokens
        :param stop_words: a list of stop words
        :return: a list of tokens without stop words
    """
    if not (isinstance(tokens, list) and len(tokens) != 0):
        return None
    else:
        new_tokens = []
        for i in tokens:
            if not (i in stop_words):
                new_tokens.append(i)
        return new_tokens



def calculate_frequencies(tokens: list) -> dict or None:
    """
        Calculates frequencies of given tokens
        :param tokens: a list of tokens
        :return: a dictionary with frequencies
    """
    k = 0
    if not (isinstance(tokens, list) and len(tokens) != 0):
        return None
    else:
        for i in tokens:
            if i is None:
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


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
        Returns the most common words
        :param freq_dict: a dictionary with frequencies
        :param top_n: a number of the most common words
        :return: a list of the most common words
    """
    if not (isinstance(freq_dict, dict)):
        return None
    else:
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
                    numb=nums[i]
                    nums[i]=nums[j]
                    nums[j]=numb

                    k=keys[i]
                    keys[i] = keys[j]
                    keys[j] = k
        if top_n > len(keys):
            return keys
        else:
            for i in range(top_n):
                new_keys.append(keys[i])
            return new_keys



def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
        Creates a language profile
        :param language: a language
        :param text: a text
        :param stop_words: a list of stop words
        :return: a dictionary with three keys – name, freq, n_words
    """
    if not (isinstance(language,str) and isinstance(text, str) \
            and isinstance(stop_words, list)):
        return None
    else:
        profile = {}
        tokens=tokenize(text)
        tokens=remove_stop_words(tokens, stop_words)
        dictionary=calculate_frequencies(tokens)
        profile['name']=language
        profile['freq']=dictionary
        profile['n_words']= len(dictionary.keys())
        return profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
        Compares profiles and calculates the distance using top n words
        :param unknown_profile: a dictionary
        :param profile_to_compare: a dictionary
        :param top_n: a number of the most common words
        :return: the distance
    """
    if not (isinstance(unknown_profile, dict) and isinstance(unknown_profile, dict) \
            and isinstance(top_n, int)):
        return None
    else:
        unk_dict = get_top_n_words(unknown_profile.get('freq'), top_n)
        com_dict = get_top_n_words(profile_to_compare.get('freq'), top_n)
        res = 0
        for i in unk_dict:
            if i in com_dict:
                res = res + 1
        return float("{0:.2f}".format(res / top_n))



def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) \
        -> str or None:
    """
        Detects the language of an unknown profile
        :param unknown_profile: a dictionary
        :param profile_1: a dictionary
        :param profile_2: a dictionary
        :param top_n: a number of the most common words
        :return: a language
    """
    if not (isinstance(unknown_profile, dict) and isinstance(profile_1, dict) \
            and isinstance(profile_2, dict) and isinstance(top_n, int)):
        return None
    else:
        prof_1_num = compare_profiles(unknown_profile, profile_1, top_n)
        prof_2_num = compare_profiles(unknown_profile, profile_2, top_n)
        if prof_1_num>prof_2_num:
            return profile_1.get('name')
        if prof_1_num<prof_2_num:
            return profile_2.get('name')
        if profile_1.get('name')>profile_2.get('name'):
            return profile_1.get('name')
        else:
            return profile_2.get('name')


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int):
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """



def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int):
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """



def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """



def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """

