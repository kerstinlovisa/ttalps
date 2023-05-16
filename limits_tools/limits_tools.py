from math import sqrt, pi

from ROOT import TGraphAsymmErrors

import physics as ph

tiny_scale = 1e9
large_scale = 1e3

regions_to_mask = {
    # "rho/omega": (0.74, 0.82),
    # "phi": (0.97, 1.07),
    "j/psi": (2.94, 3.24),
    "psi": (3.50, 3.86),
    # "z": (86.63, 95.75),
}


# with all couplings on
alp_cross_section_all_couplings_on = {
# mass (GeV), x_sec (pb)
    0.1:  3.102,
    0.2: 3.066,
    0.3: 3.075,
    0.315: 3.122,
    0.5: 3.098,
    1.0: 3.104,
    2.0: 3.087,
    4.0: 3.057,
    8.0: 3.023,
    8.5: 3.086,
    10.: 3.046,
    20.: 2.993,
    40.: 2.870,
    50.: 2.799,
    70.: 2.622,
    80.: 2.518,
    # 90.: 2.424,
}

# with only alp-top couplings on (cu = -0.5, cq = 0.5)
alp_cross_section_only_top_coupling = {
# mass (GeV), x_sec (pb)
    0.1:  0.1188,
    1.0: 0.1169,
    10.: 0.1148,
    40.: 0.09168,
    50.: 0.0844,
    80.: 0.06463,
}


def find_lifetime_for_mass(mass, coupling, Lambda, boost=False):
    ctau = ph.ctaua(mass, coupling, coupling, Lambda)  # in cm
    
    if boost:
        boost = 1 / mass
        
        if mass < 3:
            boost *= 223
        elif mass < 20:
            boost *= 230
        elif mass < 30:
            boost *= 240
        elif mass < 50:
            boost *= 260
        else:
            boost *= 296
        
        ctau *= boost
    
    ctau *= 10  # cm -> mm
    
    return ctau


def find_lifetime_for_mass_mumuonly_noboost(mass, coupling, Lambda):
    lscs = ph.getLSfromctt(coupling, coupling, Lambda, mass)
    gamma_mumu = ph.Gammaatoll(mass, ph.readCmumu(lscs), ph.sm['mmu'], Lambda)
    
    if gamma_mumu == 0:
        return 999999
    
    lifetime_mumu = ph.sm["c"] * ph.sm["hbar"] / gamma_mumu
    lifetime_mumu *= 10  # convert to mm
    
    return lifetime_mumu


def get_theory_lifetime_vs_mass_mumu_only():
    graph = TGraph()
    graph.SetLineColor(kRed)
    
    for i_mass, mass in enumerate(linspace(0, 10)):
        graph.SetPoint(i_mass, mass, find_lifetime_for_mass_mumuonly_noboost(mass, coupling, Lambda))
    
    return graph


def mass_to_lifetime(input_graph, coupling, Lambda):
    if input_graph is None:
        return None
    
    output_graph = TGraphAsymmErrors()
    
    for i in range(input_graph.GetN()):
        mass = input_graph.GetPointX(i)
        x_sec = input_graph.GetPointY(i)
        x_sec_up = input_graph.GetErrorYhigh(i)
        x_sec_down = input_graph.GetErrorYlow(i)
        
        lifetime = find_lifetime_for_mass(mass, coupling, Lambda)
        
        output_graph.SetPoint(i, lifetime, x_sec)
        output_graph.SetPointError(i, 0, 0, x_sec_down, x_sec_up)
    
    return output_graph


def find_coupling_for_cross_section(x_sec, mass):
    coeffs = {
        0.1: 0.1177,
        0.2: 0.1192,
        0.3: 0.1173,
        0.315: 0.1183,
        0.35: 0.11790,
        0.5: 0.1186,
        0.9: 0.1170,
        1: 0.1171,
        1.25: 0.1176,
        2: 0.1180,
        4: 0.1178,
        8: 0.1165,
        8.5: 0.1170,
        10: 0.1143,
        20: 0.1090,
        40: 0.0923,
        50: 0.0848,
        70: 0.0715,
        80: 0.0652,
    }
    
    couping = x_sec / coeffs[mass]
    couping = sqrt(couping)
    return couping


def cross_section_to_coupling(input_graph):
    if input_graph is None:
        return None
    
    output_graph = TGraphAsymmErrors()
    
    for i in range(input_graph.GetN()):
        mass = input_graph.GetPointX(i)
        x_sec = input_graph.GetPointY(i)
        x_sec_up = input_graph.GetErrorYhigh(i)
        x_sec_down = input_graph.GetErrorYlow(i)
        
        coupling = find_coupling_for_cross_section(x_sec, mass)
        coupling_up = find_coupling_for_cross_section(x_sec_up, mass) if x_sec_up > 0 else 0
        coupling_down = find_coupling_for_cross_section(x_sec_down, mass) if x_sec_down > 0 else 0
        
        output_graph.SetPoint(i, mass, coupling)
        output_graph.SetPointError(i, 0, 0, coupling_down, coupling_up)
    
    return output_graph