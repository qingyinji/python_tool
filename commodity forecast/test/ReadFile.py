

def readfile(path, data):
    fp = open(path, "r")
    for line in fp.readlines():
        line = line.strip()
        formline = line.split('\t')
        if (int(formline[1], 16)+int(formline[3], 16)) == 0:
            data.append(0)
            continue
        data.append((int(formline[0], 16) + int(formline[1], 16)*256) + (int(formline[2], 16) + int(formline[3], 16)*256) - (int(formline[4], 16) + int(formline[5], 16)*256))
    fp.close()
    if data[len(data)-1] != 0:
        data.append(0)
    return

