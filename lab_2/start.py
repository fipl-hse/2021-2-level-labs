"""
Language detection starter
"""

import os
from lab_1.main import tokenize, remove_stop_words
from lab_2.main import get_freq_dict, get_language_profiles, \
    get_language_features, get_text_vector, \
    calculate_distance, predict_language_score, \
    calculate_distance_manhattan, predict_language_knn


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

    lat_tokens = remove_stop_words(tokenize(LAT_TEXT), [])
    de_tokens = remove_stop_words(tokenize(DE_TEXT), [])
    eng_tokens = remove_stop_words(tokenize(EN_TEXT), [])
    unknown_tokens = []

    print(get_freq_dict(lat_tokens))
    print(get_freq_dict(de_tokens))
    print(get_freq_dict(eng_tokens))

    labels = ['eng', 'de', 'lat']
    corpus = [eng_tokens, de_tokens, lat_tokens]
    language_profiles = get_language_profiles(corpus, labels)

    list_of_unique_words = get_language_features(language_profiles)

    known_text_vectors = []
    unknown_text_vectors = []
    language_labels = []
    for text in DE_SAMPLES:
        tokens = remove_stop_words(tokenize(text), [])
        known_text_vectors.append(get_text_vector(tokens, language_profiles))
        language_labels.append('de')
    for text in EN_SAMPLES:
        tokens = remove_stop_words(tokenize(text), [])
        known_text_vectors.append(get_text_vector(tokens, language_profiles))
        language_labels.append('en')
    for text in LAT_SAMPLES:
        tokens = remove_stop_words(tokenize(text), [])
        known_text_vectors.append(get_text_vector(tokens, language_profiles))
        language_labels.append('lat')
    for token in unknown_tokens:
        unknown_text_vectors.append(get_text_vector(token, language_profiles))

    minimal_vectors = len(min(known_text_vectors, key=len))
    new_vectors = []
    for vector in known_text_vectors:
        new_vectors.append(vector[:minimal_vectors])
    unknown_text_vectors = []
    for text in UNKNOWN_SAMPLES:
        tokens = remove_stop_words(tokenize(text), [])
        unknown_text_vectors.append(get_text_vector(tokens, language_profiles))
    new_unknown_text_vectors = []
    for vector in unknown_text_vectors:
        new_unknown_text_vectors.append(vector[:minimal_vectors])

    distance = calculate_distance(new_unknown_text_vectors[0], new_vectors[0])

    distance_manhattan = calculate_distance_manhattan(new_unknown_text_vectors[0],
                                                      new_vectors[0])

    predict_language_score = predict_language_score(new_unknown_text_vectors[0],
                                                    new_vectors, language_labels)
    print(predict_language_score)

    RESULT = []
    for vector in new_unknown_text_vectors:
        RESULT.append(predict_language_knn(vector, new_vectors,
                                           language_labels, 3)[0])
    print(RESULT)
    print(EXPECTED)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, EXPECTED
