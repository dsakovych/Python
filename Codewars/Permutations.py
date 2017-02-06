def local_perm(string, value):
    lst = list()
    for i in range(len(string) + 1):
        lst.append(string[:i]+str(value)+string[i:])
    return lst

def permutations(string):
    for i in range(len(string)):
        if i == 0:
            tmp = [string[i]]
            continue
        tmp1 = []
        for item in tmp:
            tmp1 += local_perm(item, string[i])
        tmp = tmp1
    return list(set(tmp))
