import copy


def readfile(path, data, *args):
    fp = open(path, "r")
    temp = []

    if args:
        for line in fp.readlines():
            line = line.strip()
            if args[0] == 0:
                formline = line.split(',')
            else:
                formline = line.split('\t')
            if (int(formline[1]) + int(formline[3])) == 0:
                data.append(copy.deepcopy(temp))
                temp.clear()
                continue
            temp.append(int(formline[0]) + int(formline[1]) - int(formline[2]))
    else:
        for line in fp.readlines():
            line = line.strip()
            formline = line.split('\t')
            if (int(formline[1], 16)+int(formline[3], 16)) == 0:
                data.append(copy.deepcopy(temp))
                temp.clear()
                continue
            temp.append((int(formline[0], 16) + int(formline[1], 16)*256) + (int(formline[2], 16) + int(formline[3], 16)*256) - (int(formline[4], 16) + int(formline[5], 16)*256))
        fp.close()

    if len(temp) > 0:
        data.append(copy.deepcopy(temp))
    return

