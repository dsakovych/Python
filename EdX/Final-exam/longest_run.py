def longest_run(L):
    temp_incr = mIncreasing(L)
    temp_decr = mDecreasing(L)
    result = 0
    if len(temp_incr) > len(temp_decr) :
        for i in temp_incr:
            result += i
    elif len(temp_incr) == len(temp_decr) :
        for i in L:
            if sum(temp_incr) == sum(temp_decr):
                for r in temp_incr:
                    result += r
                break
            if i in temp_incr and not i in temp_decr:
                for j in temp_incr:
                    result += j
                break
            elif i in temp_decr and not i in temp_incr:
                for k in temp_decr:
                    result += k
                break

    elif len(temp_incr) < len(temp_decr):
        for i in temp_decr:
            result += i
    return result


def mIncreasing(L):
    current_set = L[:]
    temp_set = [current_set[0]]
    m_increasing = []

    for i in range(len(current_set)-1):
        if current_set[i] <= current_set[i+1]:
            temp_set.append(current_set[i+1])
            if len(temp_set) > len(m_increasing):
                m_increasing = temp_set[:]
        elif current_set[i] > current_set[i+1]:
            temp_set = [current_set[i+1]]
    return m_increasing



def mDecreasing(L):
    current_set = L[:]
    temp_set = [current_set[0]]
    m_decreasing = []
    for i in range(len(current_set)-1):
        if current_set[i] >= current_set[i+1]:
            temp_set.append(current_set[i+1])
            if len(temp_set) > len(m_decreasing):
                m_decreasing = temp_set[:]
        elif current_set[i] < current_set[i+1]:
            temp_set = [current_set[i+1]]
    return m_decreasing
