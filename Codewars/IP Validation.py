def is_valid_IP(strng):
    string = strng.split('.')
    if len(string) == 4:
        try:
            for num in string:
                if " " in num or (num[0] == "0" and len(num) > 1): return False
                else:
                    num = int(num)
                    if num > 255 or num < 0:
                        return False
            return True
        except: return False
    return False
