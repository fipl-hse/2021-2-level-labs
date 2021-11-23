# import re
# text = 'The first% sentence><. The sec&*ond sent@ence #.'
# # text = 'The, first sentence - nice. The second sentence: bad!'
# text=list(text)
# new_text=''
#
# for i,item in enumerate(text):
#     if item.isalpha()==True or item.isdigit()==True or (item in ['.', '!', '?', ' ']):
#         new_text=new_text+item
#
# sentence_list=re.split('[.?!]\s',new_text)
#
# print(new_text)
#
# for i,sentence in enumerate(sentence_list):
#     reg_sentence=[]
#     sentence=sentence.lower()
#     sentence=re.split('\s', sentence)
#     print(sentence,"se")
#     for j,word in enumerate(sentence):
#         if word.isalpha():
#             print(word, '1')
#             reg_word = ['_']
#             word=list(word)
#             for l, letter in enumerate(word):
#                 if letter.isalpha():
#                     reg_word.append(letter)
#             reg_word.append('_')
#             reg_sentence.append(tuple(reg_word))
#     sentence_list[i]=tuple(reg_sentence)
# result = tuple(sentence_list)
# print(result)
#
#
# # for i, item in enumerate(tup_text):
# #     if (item in ('.', '?', '!', '...')) and (tup_text[i+1]==' ') and (tup_text[i+2].isuper()):
# #         for j in range(i):
# #             sentence_list[]
# #
# #
# # print(tup_text[tup_text.index('h')+1])
# # result=()
# # wordtupl=()
# # wordtupl[0]="_"
# # count=0
# # for i in text:
# #     if i.isalpha():
# #         wordtupl[count]=i
# #     elif (i in (" ",",",".","!","?")) and (i+1).isupper():
# #         wordtupl[("_")
# #         result[i]=wordtupl
#
#
