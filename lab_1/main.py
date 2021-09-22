"""
Lab 1
Language detection
"""


def tokenize():

    english_text = """A man walks into a bar and orders a glass of water. 
                          The bartender points a gun at him and the man thanks him and leaves.
                          Why did the man thank the bartender?"""

    german_text = """Stell dir vor, du bist der Kapitän eines Frachtschiffes, das 30 Meter lang und 5 Meter breit ist.
                         Voll beladen hat es einen Tiefgang von 2 Metern, nicht beladen nur von einem Meter. 
                         Seine Höchstgeschwindigkeit betägt 18 Knoten. Wie alt ist der Kapitän?"""

    unknown_text = """A man is lying in his bed, trying to sleep. 
                          He picks up the phone and makes a call.
                          He waits for a while and hangs up before anyone could answer the phone.
                          Then he sleeps peacefully."""
    import re

    english_text_lower = english_text.lower()
    german_text_lower = german_text.lower()
    unknown_text_lower = unknown_text.lower()

    english_text_lower = re.sub(r'[^a-z ]', '', str(english_text_lower))
    english_text_tokens = english_text_lower.split()

    german_text_lower = re.sub(r'[^a-zäöüß ]', '', str(german_text_lower))
    german_text_tokens = german_text_lower.split()

    unknown_text_lower = re.sub(r'[^a-zäöüß ]', '', str(unknown_text_lower))
    unknown_text_tokens = unknown_text_lower.split()

    print(english_text_tokens)
    print(german_text_tokens)
    print(unknown_text_tokens)
tokenize()

    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

def remove_stop_words():
    stop_words_eng = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during',
                      'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours',
                      'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as',
                      'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his',
                      'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our',
                      'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at',
                      'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves',
                      'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he',
                      'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after',
                      'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how',
                      'further', 'was', 'here', 'than']
    clean_eng_text = english_text_tokens[:]
    for word in clean_eng_text:
        if word in stop_words_eng:
            clean_eng_text.remove(word)
    print(clean_eng_text)

    stop_words_ge = ['aber', 'als', 'am', 'an', 'auch', 'auf', 'aus', 'bei', 'bin', 'bis', 'bist', 'da', 'dadurch',
                     'daher', 'darum', 'das', 'daß', 'dass', 'dein', 'deine', 'dem', 'den', 'der', 'des', 'dessen',
                     'deshalb', 'die', 'dies', 'dieser', 'dieses', 'doch', 'dort', 'du', 'durch', 'ein', 'eine',
                     'einem', 'einen', 'einer', 'eines', 'er', 'es', 'euer', 'eure', 'für', 'hatte', 'hatten',
                     'hattest', 'hattet', 'hier', 'hinter', 'ich', 'ihr', 'ihre', 'im', 'in', 'ist', 'ja', 'jede',
                     'jedem', 'jeden', 'jeder', 'jedes', 'jener', 'jenes', 'jetzt', 'kann', 'kannst', 'können', 'könnt',
                     'machen', 'mein', 'meine', 'mit', 'muß', 'mußt', 'musst', 'müssen', 'müßt', 'nach', 'nachdem',
                     'nein', 'nicht', 'nun', 'oder', 'seid', 'sein', 'seine', 'sich', 'sie', 'sind', 'soll', 'sollen',
                     'sollst', 'sollt', 'sonst', 'soweit', 'sowie', 'und', 'unser', 'unsere', 'unter', 'vom', 'von',
                     'vor', 'wann', 'warum', 'was', 'weiter', 'weitere', 'wenn', 'wer', 'werde', 'werden', 'werdet',
                     'weshalb', 'wie', 'wieder', 'wieso', 'wir', 'wird', 'wirst', 'wo', 'woher', 'wohin', 'zu', 'zum',
                     'zur', 'über']

    clean_ge_text = german_text_tokens[:]
    for word in clean_ge_text:
        if word in stop_words_ge:
            clean_ge_text.remove(word)
    print(clean_ge_text)

remove_stop_words()

    """
    Removes stop words
    :param tokens: a lst of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    pass


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    pass


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    pass


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def calculate_distance(profile_1: dict, profile_2: dict, top_n: int) -> float or None:
    """
    Calculates the distance using top n words
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a proportion
    """
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :return: a language
    """
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :return: a language
    """
    pass


def create_report(unknown_profile: dict, profiles: list, languages: list) -> list or None:
    """
    Creates a report on language detection
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :return: a list of dictionaries with two keys – name, score
    """
    pass


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
