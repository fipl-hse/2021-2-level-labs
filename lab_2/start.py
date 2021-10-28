"""
Language detection starter
"""

import os
import main

# PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
# PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')
# PATH_TO_PROFILE_FOLDER = os.path.join(PATH_TO_LAB_FOLDER,'profiles')

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')
PATH_TO_DATASET_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'dataset')


# C:\\Users\\krichevskiy\\Downloads\\2021-2-level-labs-main\\2021-2-level-labs-main\\lab_2\\profiles

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'eng.txt'),
              'r', encoding='utf-8') as file_to_read:
        EN_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'de.txt'),
              'r', encoding='utf-8') as file_to_read:
        DE_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'lat.txt'),
              'r', encoding='utf-8') as file_to_read:
        LAT_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_de.txt'),
              'r', encoding='utf-8') as file_to_read:
        DE_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_eng.txt'),
              'r', encoding='utf-8') as file_to_read:
        EN_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_lat.txt'),
              'r', encoding='utf-8') as file_to_read:
        LAT_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'unknown_samples.txt'),
              'r', encoding='utf-8') as file_to_read:
        UNKNOWN_SAMPLES = file_to_read.read().split('[TEXT]')[1:]


    EXPECTED = ['de', 'eng', 'lat']
    RESULT = []
    STOP_WORDS = []
    KNN = 3
    known_text_corpus = []
    language_labels = []
    # work with known texts
    # get known_text_corpus with the de, en, lat texts and language_labels
    for de_text in DE_SAMPLES:
        known_text_corpus.append(main.remove_stop_words(main.tokenize(de_text), STOP_WORDS))
        language_labels.append('de')
    for en_text in EN_SAMPLES:
        known_text_corpus.append(main.remove_stop_words(main.tokenize(en_text), STOP_WORDS))
        language_labels.append('eng')
    for lat_text in LAT_SAMPLES:
        known_text_corpus.append(main.remove_stop_words(main.tokenize(lat_text), STOP_WORDS))
        language_labels.append('lat')
    # get language_profiles


    #print(mock.called)
    language_profiles = main.get_language_profiles(known_text_corpus, language_labels)

    # get known_text_vectors
    known_text_vectors = [main.get_text_vector(text, language_profiles) for text in known_text_corpus]
    #print(known_text_vectors)
    # work with unknown texts
    for unk_text in UNKNOWN_SAMPLES:
        # tokenize unknown text and remove stop words in it
        unknown_text = main.remove_stop_words(main.tokenize(unk_text), STOP_WORDS)
        # build a sparse vector of unknown text
        unknown_text_vector = main.get_text_vector(unknown_text, language_profiles)
        # predict the language of unknown text
        prediction_unknown_languages = main.predict_language_knn(unknown_text_vector,
                                                                   known_text_vectors,
                                                                   language_labels,
                                                                   KNN)
        #print(prediction_unknown_languages)
        # get language_labels_counts of unknown texts and check the result
        RESULT.append(prediction_unknown_languages[0])
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
    assert EXPECTED == RESULT, 'Detection not working'
