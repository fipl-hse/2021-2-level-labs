"""
Language detection starter
"""

import os
import main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')
PATH_TO_PROFILE_FOLDER = os.path.join(PATH_TO_LAB_FOLDER,'profiles')



if __name__ == '__main__':

    with open('C:\\Users\\krichevskiy\\Downloads\\2021-2-level\
    -labs-main\\2021-2-level-labs-main\\lab_2\\profiles\\eng.txt', 'r', encoding='utf-8') as file_to_read:
        en_text = file_to_read.read()

    with open('C:\\Users\\krichevskiy\\Downloads\\2021-2-level\
    -labs-main\\2021-2-level-labs-main\\lab_2\\profiles\\de.txt', 'r', encoding='utf-8') as file_to_read:
        de_text = file_to_read.read()

    with open('C:\\Users\\krichevskiy\\Downloads\\2021-2-level\
    -labs-main\\2021-2-level-labs-main\\lab_2\\profiles\\lat.txt', 'r', encoding='utf-8') as file_to_read:
        la_text = file_to_read.read()

    with open('unknown.txt', 'r', encoding='utf-8') as file_to_read:
        unknown_text = file_to_read.read()

    # print(main.get_freq_dict(main.tokenize(de_text)))

    # corpus = [main.tokenize(en_text), main.tokenize(de_text), main.tokenize(la_text)]
    # labels = ['eng', 'de', 'la']

    corpus = [
        ['the', 'boy', 'is', 'playing', 'football'],
        ['der', 'junge', 'der', 'fussball', 'spielt']
    ]
    labels = ['eng', 'de']

    profiles = main.get_language_profiles(corpus, labels)
    print(profiles)
    print(main.get_language_features(profiles))
    # 4
    original_text = ['this', 'boy', 'is', 'playing', 'football']
    print(main.get_text_vector1(original_text, profiles))

    # 5
    unknown_text_vector = [0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0]
    known_text_vector = [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0]
    print(main.calculate_distance(unknown_text_vector, known_text_vector))

    # 6
    unknown_text_vector = [0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0]
    known_text_vectors = [
        [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0],
        [0.1, 0, 0.4, 0.1, 0, 0, 0.34, 0.3, 0],
        [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0.35]
    ]
    language_labels = ['eng', 'de', 'eng']

    print(main.predict_language_score(unknown_text_vector, known_text_vectors, language_labels))

    # 7
    print(main.calculate_distance_manhattan(unknown_text_vector, known_text_vectors[0]))

    # 8
    unknown_text_vector = [0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0]
    known_text_vectors = [
        [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0],
        [0.1, 0, 0.4, 0.1, 0, 0, 0.34, 0.3, 0],
        [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0.35],
        [0.11, 0, 0.34, 0.1, 0.12, 0, 0.8, 0.1234, 0.1],
        [0.1, 0, 0.4, 0.1, 0.1, 0.11, 0.34, 0.3, 0],
        [0, 0, 0.4, 0, 0, 0, 0.6, 0.3, 0.3456]
    ]
    language_labels = ['eng', 'eng', 'eng', 'eng', 'de', 'de']
    k = 3
    metric = 'euclid'

    print(main.predict_language_knn(unknown_text_vector, known_text_vectors, language_labels, k, metric))
