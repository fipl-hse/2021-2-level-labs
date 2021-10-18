list_of_distances=[0.73491, 0.45782, 0.814, 0.65523, 0.43784, 0.6996]
language_labels=['eng', 'de', 'eng', 'eng', 'de', 'de']
newdict={}
for i in range(len(list_of_distances)):
    newdict[language_labels[i]]=list_of_distances[i]
print(newdict)