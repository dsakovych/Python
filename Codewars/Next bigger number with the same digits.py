def next_bigger(n):
    string = list(str(n))
    for i in range(len(string) - 1, -1, -1):
        if int(string[i - 1]) > int(string[i]): continue
        else:
            string[i:] = sorted(string[i:])
            for j in range(i,len(string),1):
                if int(string[i-1]) >= int(string[j]): continue
                else: 
                    string.insert(i-1,string[j])
                    del string[j + 1]
                    string[i:] = sorted(string[i:])
                    return int("".join(string))
    return -1
