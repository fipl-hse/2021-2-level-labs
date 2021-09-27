"""
Lab 1
Language detection
"""

text_str = '''Studentenleben

Ich bin Student, ich studiere Germanistik an der Uni. Mein Tag fängt ziemlich früh an: Normalerweise stehe ich um halb 7 auf, aber während der Prüfungsperiode muss ich noch früher aufstehen, um für die Prüfungen zu pauken.

Ich wohne nicht im Wohnheim, sondern zu Hause bei den Eltern. Das ist gut und praktisch, weil ich keine Miete brauche. Aber leider liegt mein Haus weit von der Uni, deshalb muss ich mit der U-Bahn fahren und noch 10 Minuten zu Fuß gehen.

Die Vorlesungen beginnen um 9 Uhr. An der Uni gibt es Studenten aus den verschiedenen Ländern. Mein Lieblinsfach ist Deutsch, denn ich liebe die Grammatik und die deutsche Sprachmelodie.

Um 13 Uhr ist eine Mittagspause, und alle gehen in die Kantine. Dort esse ich zu Mittag und plaudere mit den anderen Kommilitonen.

Nach den Vorlesungen gehe ich in die Bibliothek, um Zeitungen und Zeitschriften auf Deutsch zu lesen. Das brauche ich für die Seminare. Häufig machen ich und meine Freunde kleine Videoabende und schauen verschiedene Filme auf Deutsch an, um das Hörverstehen zu trainieren. Natürlich können wir diese Filme ohne Untertitel gucken, weil wir Deutsch schon ganz gut können.

Im Sommer werde ich ein Praktikum im Auslande machen, und ich hoffe, nach Deutschland zu fahren. Aber dafür muss ich nur gute Noten in meinem Studienbuch haben. Von Frisch noted something further. When the scout bees came home to tell their
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
revolutionise the study of animal behaviour generally. Mox novus īnfāns in cūnīs Aemiliae erit. Aemilia rūrsus īnfantem habēbit. Tum quattuor līberī in familiā erunt. Iūlius et Aemilia quattuor līberōs habēbunt. Aemilia īnfantem suum amābit. Iūlius et Aemilia īnfantem suum aequē amābunt. Annō post īnfans prīma verba discet et prīmōs grādūs faciet. Īnfāns ambulāns ā parentibus laudābitur.

Aemilia: "Ego īnfantem meum bene cūrābō: semper apud eum manēbō, numquam ab eō discēdam." Iūlius: "Certē bona māter eris, Aemilia: īnfantem tuum ipsa cūrābis nec eum apud nūtrīcem relinquēs." Aemilia: "Etiam nocte apud īnfantem erō, semper cum eō dormiam. Nōs et īnfāns in eōdem cubiculō dormiēmus." Iūlius: "Nōn dormiēmus, sed vigilābimus! Nam certē ab īnfante vāgiente excitābimur!" Aemilia: "Ego excitābor, tū bene dormiēs nec excitāberis!"

_

Salvēte amīcī!

Segōvia parvum oppidum in Hispāniā est, prope viam Rōmānam vīcēsimam quārtam (XXIV). Circum oppida multōs montēs sunt. In eā multōs virōs et multās fēminās habitant. Ūnum castellum apud villās ab iīs vidētur. Quid inest in castellum? Illīc est pulchrus hortus et multa cubicula. Castellum Segōviae antīquum est. 

Prope castellum ecclēsia est. Quoque antīqua est ea, sed nōn tam antīqua quam castellum. Ea ūnam campanam habet, quae  ab virīs verberātur et ab multīs familiīs Segōviae audiuntur.In centrō oppidī est magnus et fōrmōsus aqueductus. Ā aqueductō aqua oppidum montibus vehitur. Unde venit aqua? Ab montibus venit. Quō aqua vehitur? Ad oppidum. In Segōviā nūllī fluviī sunt; itaque aqueductus aquam oppidō dat. 

Novusne est?  Immō antiquus est, et neque castellum neque ecclēsia tam antiquī sunt quam aqueductus Rōmānus. Villae apud eum autem novae sunt. Multa oppida Rōmāna aqueductī habent, quae aquam procul ā oppidīs sumunt iīsque dant. Circum oppidum etiam mūrus antīquus est, quī trēs portās (portam Cebrianī, portam Andrēae et portam Iacobī) habet. Per eās iī quī ad oppidum eunt in Segōviam intrant. Cūr iī Segoviam eunt? Quia pulchra est! At first, von Frisch thought the bees were responding only to the scent of the food.
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

def tokenize(text_str):
       if isinstance(text_str, str) == False:
           return None
       else:
           symbols = ["'", '-', '%', '>', '<', '$', '@', '#', '&', '*', '.', ',', '!', ';', ':']
           for i in text_str:
               if i in symbols:
                   text_str = text_str.replace(i, "")
           text_update = ''.join([i for i in text_str if not i.isdigit()])
           return text_update.lower().split()

text = tokenize(text_str)
print(text)

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

    #else:
        #if text_update:
            #filtered_text = []
            #for m in text_update:
                #if m not in STOP_WORDS:
                    #filtered_text.append(m)
            #return filtered_text
        #else:
             #return None





def calculate_frequencies(text_update):



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
