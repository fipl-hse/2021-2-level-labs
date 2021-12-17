"""
Language detection starter
"""

import os
from lab_3.main import encode_corpus, LanguageProfile, LetterStorage, \
    tokenize_by_sentence, load_profile
PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles\\')

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive \
     decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen,\
     am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.\
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""
    IT_SAMPLE = "Una settimana fa noi siamo andati in Italia in due con mio marito! \
    Queste vacanze erano perfette! Abbiamo avuto solo una settimana per viaggiare, \
    ma era la settimana favolosa! Abbiamo prenotato una macchina e siamo andati da Roma a Positano."
    FR_SAMPLE = "Pour commencer, le tsar Peter First a ordonné que les vacances et \
                le début d'année soient reportés du 1er septembre au 1er janvier, \
                pour que tout se passe comme dans l'Ouest."
    AF_SAMPLE = " Op oujaarsaand word die oorgang van die ou na die nuwe gevier, \
                Die nuwe jaar word soms ingewag met kerkdienste, vuurwerke en ander feesvieringe"
    SK_SAMPLE = "O Novom roku - Nový rok je sviatok začiatku nového roka, \
    Podľa celosvetovo najrozšírenejšieho gregoriánskeho kalendára pripadá na januára"
    MK_SAMPLE = "Ова прашање е сериозно стратешко прашање на ЕУ и секое понатамошно \
                одложување ќе наштети на демократските процеси на Балканот"
    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?
    # use function encode_corpus
    # score 6-8

    # use tokenize_by_sentence
    # score 6-8
    eng_text = tokenize_by_sentence(ENG_SAMPLE)
    de_text = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_text = tokenize_by_sentence(UNKNOWN_SAMPLE)
    it_text = tokenize_by_sentence(IT_SAMPLE)
    fr_text = tokenize_by_sentence(FR_SAMPLE)
    mk_text = tokenize_by_sentence(MK_SAMPLE)
    sk_text = tokenize_by_sentence(SK_SAMPLE)
    af_text = tokenize_by_sentence(AF_SAMPLE)
    # score 10 secret_text
    secret_text = tokenize_by_sentence(SECRET_SAMPLE)

    # use method update in LetterStorage
    # score 6-8
    storage = LetterStorage()
    storage.update(eng_text)
    storage.update(de_text)
    storage.update(unk_text)
    storage.update(it_text)
    storage.update(fr_text)
    storage.update(sk_text)
    storage.update(mk_text)
    storage.update(af_text)
    # score 10
    storage.update(secret_text)
    encoded_eng_text = encode_corpus(storage, eng_text)
    encoded_de_text = encode_corpus(storage, de_text)
    encoded_unk_text = encode_corpus(storage, unk_text)


    # score 10
    encoded_secret_text = encode_corpus(storage, secret_text)

    # use LanguageProfile
    # score 6-8
    eng_profile = LanguageProfile(storage, 'en')
    de_profile = LanguageProfile(storage, 'de')
    unk_profile = LanguageProfile(storage, 'unk')
    it_profile = LanguageProfile(storage, 'it')
    sk_profile = LanguageProfile(storage, 'sk')
    mk_profile = LanguageProfile(storage, 'mk')
    fr_profile = LanguageProfile(storage, 'fr')
    af_profile = LanguageProfile(storage, 'af')
    # score 10
    secret_profile = LanguageProfile(storage, 'secret')
    RESULT = ''
    profile_en_10 = load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'en'))
    #new_profile = LanguageProfile()
    it_profile.open(os.path.join(PATH_TO_PROFILES_FOLDER, 'it'))
    sk_profile.open(os.path.join(PATH_TO_PROFILES_FOLDER, 'sk'))
    mk_profile.open(os.path.join(PATH_TO_PROFILES_FOLDER, 'mk'))
    fr_profile.open(os.path.join(PATH_TO_PROFILES_FOLDER, 'fr'))
    af_profile.open(os.path.join(PATH_TO_PROFILES_FOLDER, 'af'))

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
