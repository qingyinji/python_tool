start = 3
param = 0.9


def errordate(data_input):
    index = -1
    for _ in data_input:
        index += 1
        if _ > 1000:
            if (index > 0) and (index < len(data_input) - 1):
                data_input[index] = (data_input[index - 1] + data_input[index + 1]) / 2
            elif index == 0:
                data_input[index] = data_input[index + 1]
            elif index == len(data_input)-1:
                data_input[index] = data_input[index - 1]

    y1 = 0
    for i in range(len(data_input)-start):
        for j in range(start-1):
            y1 += abs(data_input[j+i+1] - data_input[j+i])
        y1 /= (start-1)
        y2 = data_input[i+start] - data_input[i+start-1]
        if abs(y2) > (y1*param):
            if y2 < 0:
                data_input[i+start] += abs(y2)
        y1 = 0

    return
