"""
Language detection starter
"""

import os
from lab_3.main import LanguageProfile, LetterStorage, ProbabilityLanguageDetector, \
    tokenize_by_sentence, encode_corpus, NGramTrie

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')
profiles = os.listdir(PATH_TO_PROFILES_FOLDER)

if __name__ == '__main__':
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""
    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?
    detector = ProbabilityLanguageDetector()
    for profile in profiles:
        known_letter_storage = LetterStorage()
        known_profile = LanguageProfile(known_letter_storage, profile)
        known_profile.open(os.path.join(PATH_TO_PROFILES_FOLDER, profile))
        detector.register_language(known_profile)
    tokenized_unk = tokenize_by_sentence(SECRET_SAMPLE)
    unknown_storage = LetterStorage()
    unknown_storage.update(tokenized_unk)
    encoded_unk_corpus = encode_corpus(unknown_storage, tokenized_unk)
    unknown_profile = LanguageProfile(letter_storage=unknown_storage, language_name='unk')
    unknown_profile.create_from_tokens(encoded_unk_corpus, (2,))
    probabilities = detector.detect(unknown_profile, 1000, (2,))
    final_language = ()
    for language, distance in probabilities.items():
        if not final_language:
            final_language = (language, distance)
        elif distance < final_language[1]:
            final_language = (language, distance)   
    print(final_language)
    RESULT = final_language
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
