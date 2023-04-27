import math

import physics as ph

Lambda = 1000 * 4 * math.pi
coupling = 0.5


def find_lifetime_for_mass(mass):
    ctau = ph.ctaua(mass, coupling, coupling, Lambda)  # in cm
    return ctau*10  # convert to mm


for mass in (0.1, 0.3, 0.315, 0.5, 2, 8, 10):
    print(f"{mass=}: {find_lifetime_for_mass(mass)} mm")

    gamma = ph.Gammaa(mass, coupling, coupling, Lambda)
    print(f"\t{gamma=}")

    lscs = ph.getLSfromctt(coupling, coupling, Lambda, mass)
    gamma_mumu = ph.Gammaatoll(mass, ph.readCmumu(lscs), ph.sm['mmu'], Lambda)
    print(f"\t{gamma_mumu=}")
    
    if gamma_mumu == 0:
        continue
    
    lifetime_mumu = ph.sm["c"]*ph.sm["hbar"]/gamma_mumu
    lifetime_mumu *= 10  # convert to mm
    
    
    print(f"\t{lifetime_mumu=} mm")
    


