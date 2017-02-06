def has_two_cube_sums(n):
    test_var = int(round(pow(n ,0.33333)))
    test_var1 = test_var + 1
    result = 0
    for i in range(test_var + 1):
        for j in range(test_var1):
            if n == (j + 1) ** 3 + test_var1 ** 3: result += 1       
        test_var1 = test_var - i
    return result >= 2
