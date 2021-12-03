import itertools

from utilities import load_data, submit


# Convert to list of int:
# input_data = list(map(int, input_data))


part = 1

# gamma = ''
# epsilon = ''
# for i in range(len(input_data[0])):
#     count_0 = 0
#     count_1 = 0
#     for b in input_data:
#         if b[i] == '0':
#             count_0 += 1
#         if b[i] == '1':
#             count_1 += 1
#     if count_0 > count_1:
#         gamma += '0'
#         epsilon += '1'
#     else:
#         gamma += '1'
#         epsilon += '0'
#
# answer = int(gamma, 2) * int(epsilon, 2)
#
# print(answer)
# submit(answer, part)

input_data = load_data()

# Split input into a list of str:
input_data = input_data.splitlines()

ox = ''
for i in range(12):
    count_0 = 0
    count_1 = 0
    for b in input_data:
        if b[i] == '0':
            count_0 += 1
        if b[i] == '1':
            count_1 += 1
    if count_1 >= count_0:
        keep = '1'
    else:
        keep = '0'
    keep_list = []
    for b in input_data:
        if b[i] == keep:
            keep_list.append(b)
    input_data = keep_list
    if len(input_data) == 1:
        ox = input_data[0]

input_data = load_data()

# Split input into a list of str:
input_data = input_data.splitlines()

co2 = ''
for i in range(12):
    count_0 = 0
    count_1 = 0
    for b in input_data:
        if b[i] == '0':
            count_0 += 1
        if b[i] == '1':
            count_1 += 1
    if count_1 >= count_0:
        keep = '0'
    else:
        keep = '1'
    keep_list = []
    for b in input_data:
        if b[i] == keep:
            keep_list.append(b)
    input_data = keep_list
    if len(input_data) == 1:
        co2 = input_data[0]

answer = int(ox, 2) * int(co2, 2)
print(answer)
# submit(answer, 2)
