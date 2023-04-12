import physics as ph


def find_lifetime_for_mass(mass):
    Lambda = 1000
    ctau = ph.ctaua(mass, 0.5, 0.5, Lambda)  # in cm
    return ctau*10 # convert to mm


for mass in (0.1, 0.3, 0.315, 0.5, 2, 8, 10):
    print(f"{mass=}: {find_lifetime_for_mass(mass)} mm")
