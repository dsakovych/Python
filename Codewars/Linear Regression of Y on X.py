def mean(x, y = None):
    result = 0
    try:
        for i in range(len(x)):
            result += x[i]*y[i]
        return float(result) / len(x)
    except:
        for i in range(len(x)):
            result += x[i]
        return float(result) / len(x)

def regressionLine(x, y):
    b = (mean(x,y) - mean(x) * mean(y)) / (mean(x,x) - mean(x) ** 2)
    a = mean(y) - b * mean(x)
    return round(a,4) , round(b,4)
