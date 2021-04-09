import numpy as np
x_time = [[10, 20, 5, 10, 20]]
table = []
for i in range(30):
    num_all = 0
    num_part = 0
    for j in range(len(x_time)):
        try:
            num_all += x_time[j][i]
        except IndexError:
            continue
        num_part += 1
    if num_part == 0:
        break
    table.append(num_all / num_part)
print(table)