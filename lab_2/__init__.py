
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
        return distance

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
unknown_text_vector = [0.55, 0.1, 0.2, 0.5, 0.4, 0.2, 0.29, 0.1, 0.18]
known_text_vectors = [[0.4, 0.1, 0.4, 0.3, 0, 0.21, 0.11, 0.13, 0],
                               [0.11, 0.45, 0.4, 0.28, 0, 0.12, 0.62, 0.21, 0.35],
                               [0.11, 0.28, 0, 0.1, 0.11, 0.49, 0.23, 0.3, 0.43],
                               [0.13, 0, 0.24, 0.41, 0.12, 0.13, 0.56, 0.14, 0.1],
                               [0.18, 0, 0.2, 0.15, 0.1, 0.11, 0.35, 0.34, 0],
                               [0.15, 0, 0.4, 0.21, 0, 0.09, 0.24, 0.33, 0]]
language_labels = ['en', 'en', 'de', 'en', 'de', 'de']
k = 4
metric = 'euclid'

list_of_distances = []
if metric == 'euclid':
    for i in known_text_vectors:
        distance = calculate_distance(unknown_text_vector, i)
        list_of_distances.append(distance)
elif metric == 'manhattan':
    for i in known_text_vectors:
        distance = calculate_distance_manhattan(unknown_text_vector, i)
        list_of_distances.append(distance)
print(list_of_distances, language_labels)
for i in range(len(list_of_distances) - 1):
    for j in range(i , len(list_of_distances)):
        if list_of_distances[i] > list_of_distances[j]:
            n = list_of_distances[i]
            list_of_distances[i] = list_of_distances[j]
            list_of_distances[j] = n

            x = language_labels[i]
            language_labels[i] = language_labels[j]
            language_labels[j] = x
print(list_of_distances,language_labels)
srez_of_distances=list_of_distances[:k]
srez_of_labels=language_labels[:k]
helper_labels=srez_of_labels
count=0
mas=[]
for i in srez_of_labels:
    curr_frequency = srez_of_labels.count(i)
    mas.append(curr_frequency)
newz=dict(zip(srez_of_labels,mas))
print(newz)
top_frequences_srez=list(newz.values())
top_labeles_srez=list(newz.keys())
print(top_labeles_srez)
for i in range(len(top_frequences_srez) - 1):
    for j in range(i , len(top_frequences_srez)):
        if top_frequences_srez[i] < top_frequences_srez[j]:
            n = top_frequences_srez[i]
            top_frequences_srez[i] = top_frequences_srez[j]
            top_frequences_srez[j] = n

            x = top_labeles_srez[i]
            top_labeles_srez[i] = top_labeles_srez[j]
            top_labeles_srez[j] = x
print(top_frequences_srez,top_labeles_srez)
print(newz)

max_top_labels_srez=[]
for i in top_frequences_srez:
    if i==max(top_frequences_srez):
        print(top_frequences_srez.index(i))
        max_top_labels_srez.append(top_labeles_srez[top_frequences_srez.index(i)])
        print(max_top_labels_srez,i)
print(max_top_labels_srez)
rlist=[]
if len(max_top_labels_srez)==1:
    rlist.append(max_top_labels_srez[0])
    rlist.append(min(srez_of_distances))
    print(rlist)
for i in max_top_labels_srez:
    result_distance = min(srez_of_distances)
    num=srez_of_distances.index(min(srez_of_distances))
    name=srez_of_labels[num]
    print(rlist)

# for i in srez_of_labels:
#     curr_frequency=srez_of_labels.count(i)
#     print(i,curr_frequency)
#     if curr_frequency > count:
#         count=curr_frequency
#         name=i
#         result_distance=min(srez_of_distances)
# if count==0:
#     result_distance=min(srez_of_distances)
#     num=srez_of_distances.index(min(srez_of_distances))
#     name=srez_of_labels[num]

#rlist=[name,result_distance]

# print(name,result_distance)
# print(rlist)





