"""
Programming 2021
Seminar 1
Debugging
"""


# Three main ideas:
# 1. Python is a program that launches another program.
#       We pass the code from main.py into the python virtual machine (PVM),
#           where it is executed. For example, >>> python main.py
# 2. Reading the output in the terminal after executing the program will help you
#       find the error. Everything is told in the terminal output,
#           the main thing is to look carefully.
# 3. Debugging is the first skill of a programmer.
#       It helps you to take a step-by-step look at how the program works.


# Debugging exercise. Debug the program and fix errors:
first_num = 15
second_num = 30

collection = [first_num, second_num]
print(f'Collection of numbers: {collection}')


# Case1: the first exception trigger:
third_num = collection[2]

# Fix the first exception:
# third_num = 0
# collection.append(third_num)
# print(f'Collection with an added number: {collection}')


# Case 2: the second exception trigger:
if (first_num + second_num) / third_num == 1:
    print('First number + second equals third number')
else:
    print('First number + second does not equal third number')
print('Program finished')
