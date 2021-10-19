"""
Language detection starter
"""

import os
from lab_2.main import (tokenize, remove_stop_words, get_language_profiles,
                        get_text_vector, predict_language_knn)

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
    texts_corpus = []
    language_labels = []
    k = 3
    for text in DE_SAMPLES:
        texts_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('de')
    for text in EN_SAMPLES:
        texts_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('eng')
    for text in LAT_SAMPLES:
        texts_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('lat')
    language_profiles = get_language_profiles(texts_corpus, language_labels)
    known_text_vectors = []
    for text in texts_corpus:
        known_text_vectors.append(get_text_vector(text, language_profiles))
    for text in UNKNOWN_SAMPLES:
        unknown_text = remove_stop_words(tokenize(text), stop_words)
        unknown_text_vector = get_text_vector(unknown_text, language_profiles)
        predicted_language = predict_language_knn(unknown_text_vector,
                                                  known_text_vectors, language_labels, k)
        RESULT.append(predicted_language[0])
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
