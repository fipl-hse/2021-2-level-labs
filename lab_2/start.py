"""
Language detection starter
"""

import os
import main

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
    RESULT = ''
    texts_corpus = []
    language_labels = []
    stop_words = []

    language_profiles = main.get_language_profiles(texts_corpus, language_labels)
    known_text_vectors = []
    for text in texts_corpus:
        known_text_vectors.append(main.get_text_vector(texts_corpus, language_profiles))

    for text in EN_SAMPLES:
        texts_corpus.append(main.remove_stop_words(main.tokenize(text), stop_words))
        language_labels.append('eng')
    for text in DE_SAMPLES:
        texts_corpus.append(main.remove_stop_words(main.tokenize(text), stop_words))
        language_labels.append('de')
    for text in LAT_SAMPLES:
        texts_corpus.append(main.remove_stop_words(main.tokenize(text), stop_words))
        language_labels.append('lat')
    for text in UNKNOWN_SAMPLES:
        unknown_text = main.remove_stop_words(main.tokenize(text), stop_words)
        unknown_text_vector = main.get_text_vector(unknown_text, language_profiles)
        predicted_language = main.predict_language_score(unknown_text_vector, known_text_vectors, language_labels)
    RESULT.append(predicted_language)
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Detection not working'
