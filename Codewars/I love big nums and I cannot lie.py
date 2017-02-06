def biggest(array):
    dublicates = set([x for x in array if array.count(x) > 1])
    array = list(map(str, array))
    max_len = max(list(map(lambda x: len(x), array)))
    result = []
    d = {}
    for item in array:
        if len(item) < max_len:
            tmp = item * int((max_len / len(item)) + 1)
            d[int(item)] = int(tmp[:max_len])
        else:
            d[int(item)] = int(item)
    while len(d) > 0:
        max1 = list(list(d.items())[0])
        for k, v in d.items():
            if v > max1[1]:
                max1[0] = k
                max1[1] = v
            elif v == max1[1]:
                if int(str(k) + str(max1[1])) >= int(str(max1[1]) + str(k)):
                    max1[0] = k
                    max1[1] = v
                else:
                    continue
            else:
                continue
        result.append(max1[0])
        if max1[0] not in dublicates:
            del d[max1[0]]
        else:
            dublicates.remove(max1[0])
    result = list(map(str, result))
    return str(int(''.join(result)))
