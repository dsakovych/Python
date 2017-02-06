def general_poly(L):
    return lambda x: sum(e*x**n for e, n in zip(L, range(len(L)-1, -1, -1)))
