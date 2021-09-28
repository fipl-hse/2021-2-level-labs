"""
Lab 1
Language detection
"""


import re
text = str(input('Enter your text: '))
def tokenize():
    if re.search(r'[^a-zA-Z\0-9üÜäÄöÖß]+[^\w\s]', text):
        None
        print('Вы ввели текст на кириллице')
    else:
        text2=text.lower()
        token = re.sub(r'[^\w\s]','',text2)
        token2 = re.split(r'\b\W\b', token)
        return token2
    
    def remove_stop_words():
        stopwords = ['am','is','are','a','an']
        stoplist =[]
        t = input('stopwords:')
        if t not in stopwords:
            None
        else:
            stoplist.append(t)
            clear_text = []
            for word in token2:
                if word not in stoplist:
                    clear_text.append(word)
                    return clear_text
                    
        def calculate_frequencies():
            freqdict = {}
            if word in clear_text:
                for word in clear_text:
                    if len(word) >= 0 and not freqdict.get(word):
                        freqdict[word] = clear_text.count(word)
                        return freqdict
            else:
                None
            
            def get_top_n_words():
                t = sorted(freqdict.items(), key=lambda kv: kv[1], reverse=True)
                return t
            get_top_n_words()
        calculate_frequencies()
    remove_stop_words()
tokenize()



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
