
def get_coefficients(p0, p1):
    a = p1[1] - p0[1]
    b = p0[0] - p1[0]
    c = a * p0[0] + b * p0[1]
    return a, b, c



a, b, c = get_coefficients([0, 3], [-2, 0])
print(a, b, c)

a, b, c = get_coefficients([-2, 0], [2, 0])
print(a, b, c)

a, b, c = get_coefficients([2, 0], [0, 3])
print(a, b, c)