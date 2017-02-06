def convert_to_mandarin(us_num):
    us_num = int(us_num)
    trans = {'0': 'ling', '1': 'yi', '2': 'er', '3': 'san', '4': 'si',
             '5': 'wu', '6': 'liu', '7': 'qi', '8': 'ba', '9': 'jiu', '10': 'shi'}
    if us_num <= 10:
        return trans.get(str(us_num))
    elif us_num <= 19:
        return trans.get('10') + ' ' + trans.get(str(us_num % 10))
    elif us_num % 10 == 0:
        return trans.get(str(int(us_num / 10))) + ' ' + trans.get('10')
    else:
        return trans.get(str(int(us_num / 10))) + ' ' + trans.get('10') + ' ' + trans.get(str(int(us_num % 10)))
