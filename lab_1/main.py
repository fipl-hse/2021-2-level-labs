"""
Lab 1
Language detection
"""
def tokenize(text_str):
       if isinstance(text_str, str) is False:
           return None
       else:
           symbols = ["'", '-', '%', '>', '<', '$', '@', '#', '&', '*', '.', ',', '!', ';', ':']
           for i in text_str:
               if i in symbols:
                   text_str = text_str.replace(i, "")
           text_update = ''.join([i for i in text_str if not i.isdigit()])
           return text_update.lower().split()

def remove_stop_words(text_update, STOP_WORDS):
    if isinstance(STOP_WORDS, list) and isinstance(text_update, list):
        if text_update:
           for m in enumerate(text_update):
               if m[1] in STOP_WORDS:
                  text_update[m[0]] = ''
           while '' in text_update:
                text_update.remove('')
           return text_update
        else:
            return None
    else:
        return None

def calculate_frequencies(text_update):
   if isinstance(text_update, list):
       for j in text_update:
           if isinstance(j, str):
               frequency_dict = {}
               for token in text_update:
                   if token not in frequency_dict:
                       frequency_dict[token] = 1
                   else:
                       frequency_dict[token] += 1
               return frequency_dict
           return None
   return None

def get_top_n_words(frequency_dict, top_n):
    if isinstance(frequency_dict, dict) and isinstance(top_n, int):
        freq_sort_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)[:top_n])
        freq_sort_list = list((freq_sort_dict).keys())
        return freq_sort_list
    else:
        return None


def create_language_profile(language: str, text_update: str, STOP_WORDS: list) -> dict or None:

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
