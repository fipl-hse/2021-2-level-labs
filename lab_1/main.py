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

    if not isinstance(text, str):
        return None

    text = re.split(r"[^\w\s]", text)
    text = "".join(text)
    text = text.lower()
    tokens = re.findall(r"\w+", text)
    return tokens


unknown_text = '''At first, von Frisch thought the bees were responding only to the scent of the food.
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

en_text = '''Von Frisch noted something further. When the scout bees came home to tell their
sisters about the food source, sometimes they would dance outside on the horizontal
entrance platform of the hive, and sometimes on the vertical wall inside. And,
depending on where they danced, the straight portion of the waggle dance would
point in different directions. The outside dance was fairly easy to decode: the straight
portion of the dance pointed directly to the food source, so the bees would merely
have to decode the distance message and fly off in that direction to find their food.
But by studying the dance on the inner wall of the hive, von Frisch discovered a
remarkable method which the dancer used to tell her sisters the direction of the food
in relation to the sun. When inside the hive, the dancer cannot use the sun, so she
uses gravity instead. The direction of the sun is represented by the top of the hive
wall. If she runs straight up, this means that the feeding place is in the same
direction as the sun. However, if, for example, the feeding place is 40º to the left of
the sun, then the dancer would run 40º to the left of the vertical line. This was to be
the first of von Frisch’s remarkable discoveries. Soon he would also discover a
number of other remarkable facts about how bees communicate and, in doing so,
revolutionise the study of animal behaviour generally. '''

de_text = '''Studentenleben

Ich bin Student, ich studiere Germanistik an der Uni. Mein Tag fängt ziemlich früh an: Normalerweise stehe ich um halb 7 auf, aber während der Prüfungsperiode muss ich noch früher aufstehen, um für die Prüfungen zu pauken.

Ich wohne nicht im Wohnheim, sondern zu Hause bei den Eltern. Das ist gut und praktisch, weil ich keine Miete brauche. Aber leider liegt mein Haus weit von der Uni, deshalb muss ich mit der U-Bahn fahren und noch 10 Minuten zu Fuß gehen.

Die Vorlesungen beginnen um 9 Uhr. An der Uni gibt es Studenten aus den verschiedenen Ländern. Mein Lieblinsfach ist Deutsch, denn ich liebe die Grammatik und die deutsche Sprachmelodie.

Um 13 Uhr ist eine Mittagspause, und alle gehen in die Kantine. Dort esse ich zu Mittag und plaudere mit den anderen Kommilitonen.

Nach den Vorlesungen gehe ich in die Bibliothek, um Zeitungen und Zeitschriften auf Deutsch zu lesen. Das brauche ich für die Seminare. Häufig machen ich und meine Freunde kleine Videoabende und schauen verschiedene Filme auf Deutsch an, um das Hörverstehen zu trainieren. Natürlich können wir diese Filme ohne Untertitel gucken, weil wir Deutsch schon ganz gut können.

Im Sommer werde ich ein Praktikum im Auslande machen, und ich hoffe, nach Deutschland zu fahren. Aber dafür muss ich nur gute Noten in meinem Studienbuch haben.'''


# unknown_text = open('unknown.txt', encoding='utf-8').read()
# en_text = open('en.txt', encoding='utf-8').read()
# de_text = open('de.txt', encoding='utf-8').read()


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None

    filt_tokens = []
    for token in tokens:
        if token not in stop_words:
            filt_tokens.append(token)
    return filt_tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if not isinstance(tokens, list):
        return None

    freq_dict = {}
    for word in tokens:
        if word not in freq_dict:
            freq_dict[word] = 1
        else:
            freq_dict[word] += 1
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None

    words = len(freq_dict)
    freq_val = reversed(sorted(freq_dict.values()))
    sorted_freq = {}

    for value in freq_val:
        for key in freq_dict.keys():
            if freq_dict[key] == value:
                sorted_freq[key] = freq_dict[key]

    if top_n > words:
        top_words = sorted_freq
        return top_words
    if top_n < words:
        top_words = list(sorted_freq.keys())[:(top_n)]
        return top_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not isinstance(language, str) or not isinstance(text, str) or not isinstance(stop_words, list):
        return None

    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    language_profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None

    top_unknown = get_top_n_words(unknown_profile['freq'], top_n)
    top_language_compare = get_top_n_words(profile_to_compare['freq'], top_n)

    compared_list = []
    for word in top_unknown:
        if word in top_language_compare:
            compared_list.append(word)

    score = round(len(compared_list)/len(top_unknown), 1)
    return score


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) \
            or not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None

    score_en = compare_profiles(unknown_profile, profile_1, top_n)
    score_de = compare_profiles(unknown_profile, profile_2, top_n)

    if score_en > score_de:
        language_unknown = profile_1['name']
    elif score_en < score_de:
        language_unknown = profile_2['name']
    else:
        prof = [profile_1['name'], profile_2['name']]
        prof = sorted(prof)
        language_unknown = prof[0]
    return language_unknown