def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    k=0
    if not isinstance(tokens, list):
        return None
    else:
        for i in tokens:
            if i is None:
                k = 1
                break
        if k == 1:
            return None
        else:
            freq_list = {}
            for i in tokens:
                if i in freq_list.keys():
                    freq_list[i] += 1
                else:
                    freq_list[i] = 1
            for i in freq_list:
                freq_list[i] = round(freq_list[i] / len(tokens), 5)
            return freq_list

corpus = [['the', 'boy', 'is', 'playing', 'football'],
                  ['der', 'junge', 'der', 'fussball', 'spielt']]
labels = ['en', 'de']
language_profiles={}
n=0
for i in corpus:
    newdict=get_freq_dict(i)
    language_profiles[labels[n]]=newdict
    n+=1
print(language_profiles)