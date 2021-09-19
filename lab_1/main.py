"""
Lab 1
Language detection
"""
import re
# import nltk

def tokenize(text: str) -> list or None:
    text = re.split(r"[^\w\s]", text)
    text = "".join(text)
    text = text.lower()
    tokens = re.findall(r"\w+", text)
    return tokens

text = '''  
At first, von Frisch thought the bees were responding only to the scent of the food.
But what did the third dance mean? And if bees were responding only to the scent,
how could they also ‘sniff down’ food hundreds of metres away from the hive*, food
which was sometimes downwind? On a hunch, he started gradually moving the
feeding dish further and further away and noticed as he did so that the dances of the
returning scout bees also started changing. If he placed the feeding dish over nine
metres away, the second type of dance, the sickle version, came into play.
But once he moved it past 36 metres, the scouts would then start dancing the third,
quite different, waggle dance.
The measurement of the actual distance too, he concluded, was precise. For
example, a feeding dish 300 metres away was indicated by 15 complete runs
through the pattern in 30 seconds. When the dish was moved to 60 metres away,
the number dropped to eleven.'''

tokenize(text)

def remove_stop_words(tokens: list, stop_words: list) -> list or None:

    for token in tokens:
        if token not in stop_words:
            filt_tokens.append(token)
            tokens = filt_tokens
    return tokens

tokens = tokenize(text)
# stop_words = nltk.corpus.stopwords.words('english')
# stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
stop_words = ['the', 'a', 'is']
filt_tokens = []

remove_stop_words(tokens, stop_words)


def calculate_frequencies(tokens: list) -> dict or None:

    for word in tokens:
        if word not in freq_dict:
            freq_dict[word] = 1
        else:
            freq_dict[word] += 1
    return freq_dict

freq_dict = {}
tokens = remove_stop_words(tokens, stop_words)

calculate_frequencies(tokens)

def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:

    for i in freq_val:
        for k in freq_dict.keys():
            if freq_dict[k] == i:
                sorted_freq[k] = freq_dict[k]

    if top_n > words:
        top_words = sorted_freq
        return top_words
    if top_n < words:
        s = list(sorted_freq.keys())[:(top_n)]
        v = list(sorted_freq.values())
        top_words = dict(zip(s, v))
        return top_words

sorted_freq = {}
new_dicts = {v: k for k, v in freq_dict.items()}
freq_dict = calculate_frequencies(tokens)
top_n = len(new_dicts)
words = len(freq_dict)
freq_val = reversed(sorted(freq_dict.values()))
sf_val = [sorted_freq.values()]

get_top_n_words(freq_dict, top_n)


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
