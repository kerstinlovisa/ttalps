from math import sqrt


def get_rlxy(x_1, x_2, y_1, y_2):
    x_2 += 1e-10
    y_2 += 1e-10
    
    return sqrt(((x_1-x_2)**2 + (y_1-y_2)**2)/((x_1+x_2)**2 + (y_1+y_2)**2))


x_1 = 0.5
x_2 = 0.5
y_1 = 0
y_2 = 0

print(f"{x_1=}, {x_2=}, {y_1=}, {y_2=}, Rlxy: {get_rlxy(x_1, x_2, y_1, y_2)}")