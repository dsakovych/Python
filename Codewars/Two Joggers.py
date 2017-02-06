import fractions
def lcm(a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0

def nbr_of_laps(x, y):
    return [lcm(x,y) / x , lcm(x,y) / y]
