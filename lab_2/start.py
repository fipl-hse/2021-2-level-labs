"""
Language detection starter
"""

import os
from lab_2.main import tokenize, remove_stop_words, get_text_vector, get_language_profiles, predict_language_score, \
    calculate_distance
PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')
PATH_TO_DATASET_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'dataset')

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

    stop_words = []
    labels = []
    known_vectors = []
    known_corpus_de = []
    known_corpus_eng = []
    known_corpus_lat = []
    # add language labels
    for text in DE_SAMPLES:
        known_corpus_de.extend(remove_stop_words(tokenize(text), stop_words))
    labels.append('de')
    for text in EN_SAMPLES:
        known_corpus_eng.extend(remove_stop_words(tokenize(text), stop_words))
    labels.append('eng')
    for text in LAT_SAMPLES:
        known_corpus_lat.extend(remove_stop_words(tokenize(text), stop_words))
    labels.append('lat')
    # get language profiles
    language_profiles = get_language_profiles([known_corpus_de, known_corpus_eng, known_corpus_lat],
                                              labels)
    # get known text vectors
    known_vectors.append(get_text_vector(known_corpus_de, language_profiles))
    known_vectors.append(get_text_vector(known_corpus_eng, language_profiles))
    known_vectors.append(get_text_vector(known_corpus_lat, language_profiles))

    for text in UNKNOWN_SAMPLES:
        unknown_text = remove_stop_words(tokenize(text), stop_words)
        unknown_text_vector = get_text_vector(unknown_text, language_profiles)
        predict_lang = predict_language_score(unknown_text_vector, known_vectors, labels)
        RESULT.append(predict_lang[0])
    print(RESULT)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert EXPECTED == RESULT, 'Detection not working'
