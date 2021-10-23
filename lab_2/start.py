"""
Language detection starter
"""

import os
from lab_1.main import tokenize, remove_stop_words
from lab_2.main import predict_language_knn, get_language_profiles, \
    get_text_vector,get_language_features

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

    language_labels = []
    stop_words = []
    known_text_vectors = []
    unknown_text_vectors = []
    known_texts_corpus = []
    texts_corpus = [EN_TEXT,DE_TEXT,LAT_TEXT]
    tokens_corpus = []

    for text in texts_corpus:
        tokens = remove_stop_words(tokenize(text), stop_words)
        tokens_corpus.append(tokens)
    language_profiles = get_language_profiles(tokens_corpus, ['eng', 'de', 'lat'])
    #print(get_language_features(language_profiles))
    #print(len(get_language_features(language_profiles)))
    #print(language_profiles)
    text_samples = {"de":DE_SAMPLES,"eng":EN_SAMPLES,"lat":LAT_SAMPLES}
    for lang, texts in text_samples.items():
        for text in texts:
            tok_text = remove_stop_words(tokenize(text),stop_words)
            known_text_vector = get_text_vector(tok_text, language_profiles)
            #print(len(known_text_vector))
            known_text_vectors.append(known_text_vector)
            language_labels.append(lang)


    for text in UNKNOWN_SAMPLES:
        unknown_text = (remove_stop_words(tokenize(text),stop_words))
        unknown_text_vectors.append(get_text_vector(unknown_text, language_profiles))
    print(predict_language_knn(unknown_text_vectors[0],known_text_vectors,language_labels, 1, 'manhattan'))


    EXPECTED = ['de', 'eng', 'lat']
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
