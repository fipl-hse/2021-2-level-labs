"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words


# 4
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


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(texts_corpus, list) and isinstance(language_labels, list)):
        return None
    else:
        for i in texts_corpus:
            if not isinstance(i,list):
                return None
        for i in language_labels:
            if not isinstance(i,str):
                return None
        language_profiles = {}
        n = 0
        for i in texts_corpus:
            newdict=get_freq_dict(i)
            language_profiles[language_labels[n]] = newdict
            n += 1
        return language_profiles







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





def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not (isinstance(original_text,list) and isinstance(language_profiles, dict)):
        return None
    else:
        text_vector = []
        features = get_language_features(language_profiles)
        for i in features:
            if i in original_text:
                for profile in language_profiles.values():
                    if i in profile.keys():
                        text_vector.append(profile[i])
            else:
                text_vector.append(0)
        return text_vector








# 6
def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    import math
    if not (isinstance(unknown_text_vector,list) and isinstance(known_text_vector,list)):
        return None
    else:
        for i in unknown_text_vector:
            if i==None:
                return None
        for i in known_text_vector:
            if i==None:
                return None
        sum=0
        for i in range(len(known_text_vector)):
            sum += ((unknown_text_vector[i])-(known_text_vector[i]))**2
        distance = round(math.sqrt(sum), 5)
        return distance



def predict_language_score(unknown_text_vector: list, known_text_vectors: list,
                           language_labels: list) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    """
    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vectors,list) and
            isinstance(language_labels, list) and len(known_text_vectors)==len(language_labels)):
        return None
    else:
        for i in unknown_text_vector:
            if i==None:
                return None
        for i in known_text_vectors:
            for j in i:
                if j==None:
                    return None
        count=0
        min=calculate_distance(unknown_text_vector, known_text_vectors[0])
        for i in known_text_vectors:
            dictance = calculate_distance(unknown_text_vector, i)
            if dictance<min:
                count +=1
                min=dictance
                metka=language_labels[count]
        prediction=[metka,min]
        return prediction





# 8
def calculate_distance_manhattan(unknown_text_vector: list,
                                 known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using manhattan metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vector: vector for known text
    """
    import math
    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vector, list)):
        return None
    else:
        for i in unknown_text_vector:
            if i == None:
                return None
        for i in known_text_vector:
            if i == None:
                return None
        distance = 0
        for i in range(len(known_text_vector)):
            distance += abs((unknown_text_vector[i]) - (known_text_vector[i]))
            distance=round(distance,5)
        return distance


def predict_language_knn(unknown_text_vector: list, known_text_vectors: list,
                         language_labels: list, k=1, metric='manhattan') -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
        using knn based algorithm and specific metric
    :param unknown_text_vector: vector for unknown text
    :param known_text_vectors: a list of vectors for known texts
    :param language_labels: language labels for each known text
    :param k: the number of neighbors to choose label from
    :param metric: specific metric to use while calculating distance
    """
    if not (isinstance(unknown_text_vector, list) and isinstance(known_text_vectors, list) and
            isinstance(language_labels, list) and isinstance(k, int) and isinstance(metric, str) and
            (len(known_text_vectors)==len(language_labels))):
        return None
    else:
        list_of_distances = []
        if metric == 'euclid':
            for i in known_text_vectors:
                distance = calculate_distance(unknown_text_vector, i)
                list_of_distances.append(distance)
        elif metric == 'manhattan':
            for i in known_text_vectors:
                distance = calculate_distance_manhattan(unknown_text_vector, i)
                list_of_distances.append(distance)
        for i in range(len(list_of_distances) - 1):
            for j in range(i, len(list_of_distances)):
                if list_of_distances[i] > list_of_distances[j]:
                    n = list_of_distances[i]
                    list_of_distances[i] = list_of_distances[j]
                    list_of_distances[j] = n

                    x = language_labels[i]
                    language_labels[i] = language_labels[j]
                    language_labels[j] = x
        srez_of_distances = list_of_distances[:k]
        srez_of_labels = language_labels[:k]
        count = 0
        for i in srez_of_labels:
            curr_frequency = srez_of_labels.count(i)
            if curr_frequency > count:
                count = curr_frequency
                name = i
                result_distance = min(srez_of_distances)
        if count == 0:
            result_distance = min(srez_of_distances)
            num = srez_of_distances.index(min(srez_of_distances))
            name = srez_of_labels[num]
        rlist = [name, result_distance]
        return rlist







# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """



def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """


def predict_language_knn_sparse(unknown_text_vector: list, known_text_vectors: list,
                                language_labels: list, k=1) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
        using knn based algorithm
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vectors: a list of sparse vectors for known texts
    :param language_labels: language labels for each known text
    :param k: the number of neighbors to choose label from
    """

