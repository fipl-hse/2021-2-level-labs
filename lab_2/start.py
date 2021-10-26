"""
Language detection starter
"""

import os
from lab_2.main import (tokenize,
                        remove_stop_words,
                        get_language_profiles,
                        get_text_vector,
                        predict_language_knn)

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

    text_corpus = []
    language_labels = []
    stop_words = []
    k = 3
    METRIC = 'manhattan'

    for text in DE_SAMPLES:
        text_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('de')
    for text in EN_SAMPLES:
        text_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('eng')
    for text in LAT_SAMPLES:
        text_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('lat')

    language_profiles = get_language_profiles(text_corpus, language_labels)
    known_text_vectors = []
    for text in text_corpus:
        known_text_vectors.append(get_text_vector(text, language_profiles))

    RESULT = []
    for text in UNKNOWN_SAMPLES:
        unknown_whole_text = remove_stop_words(tokenize(text), stop_words)
        vector_for_unknown_text = get_text_vector(unknown_whole_text, language_profiles)
        final_prediction = predict_language_knn(vector_for_unknown_text, known_text_vectors,
                                                language_labels, k, METRIC)
        RESULT.append(final_prediction[0])

    EXPECTED = ['de', 'eng', 'lat']

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT==EXPECTED, 'Detection not working'
