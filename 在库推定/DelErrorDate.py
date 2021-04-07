from typing import List
start = 3
param = 0.9


def errordate(data_input: List[float]):
    y1 = 0
    # print("inp", data_input)
    for i in range(len(data_input)-start):
        for j in range(start-1):
            y1 += abs(data_input[j+i+1] - data_input[j+i])
        y1 /= (start-1)
        y2 = data_input[i+start] - data_input[i+start-1]
        # print("y1 y2", y1, y2)
        # if abs(y2) > 2*y1:
        #     data_input[i+start] -= y2/2
        #     y2 /= 2
        if abs(y2) > (y1*param):
            if y2 < 0:
                data_input[i+start] += abs(y2)/2
        y1 = 0
    # print("inp", data_input)
    return
