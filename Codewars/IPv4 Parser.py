def to_eight_digit_binary(string):
    lst = string.split('.')
    result = []
    for i in range(len(lst)):
        lst[i] = str(bin(int(lst[i])))[2:10]
        for j in range(8 - len(lst[i])):
            lst[i] = "0" + lst[i]
        result.append(lst[i])
    return result

def ipv4__parser(ip_addr, mask):
    net_addr = []
    host_id = []
    result = []
    for i in range(4):
        var1 = ""
        var2 = ""
        for j in range(8):
            if str(to_eight_digit_binary(ip_addr)[i])[j] == "1" and str(to_eight_digit_binary(mask)[i])[j] == "1":
                var1 += "1"
            else: var1 += "0"
            if str(to_eight_digit_binary(ip_addr)[i])[j] == "1" and str(to_eight_digit_binary(mask)[i])[j] == "0":
                var2 += "1"
            else: var2 += "0"
        net_addr.append(int(var1,2))
        host_id.append(int(var2,2))
    result.append('.'.join(str(x) for x in net_addr))
    result.append('.'.join(str(x) for x in host_id))
    return tuple(result)
