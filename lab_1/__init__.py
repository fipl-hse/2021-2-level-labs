def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(language_profiles, dict) and len(language_profiles) != 0):
        return None
    else:
        features=[]
        for i in language_profiles.values():
            newdict=i
            for j in newdict:
                features.append(j)
        features.sort()
        return features
original_text = ['this', 'boy', 'is', 'playing', 'football']

language_profiles = {
    'eng': {'the': 0.2, 'boy': 0.2, 'is': 0.2, 'playing': 0.2, 'football': 0.2},
    'de': {'der': 0.4, 'junge': 0.2, 'fussball': 0.2, 'spielt': 0.2}
}
text_vector = []
features = get_language_features(language_profiles)
print(features)
for i in features:
    if i in original_text:
        for profile in language_profiles.values():
            if i in profile.keys():
                text_vector.append(profile[i])
    else:
        text_vector.append(0)
print (text_vector)
