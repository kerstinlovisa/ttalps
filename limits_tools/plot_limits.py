from math import sqrt

from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, TLegend, TGraphAsymmErrors, TBox, kWhite

import physics as ph

input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10GeV_mass-cuts_deltalxy_ratio_abs-max0p1.root"
mask_masses = True

reference_points = {
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
    90.: 2.424,
}

regions_to_mask = {
    "rho/omega": (0.74, 0.82),
    "phi": (0.97, 1.07),
    "j/psi": (2.94, 3.24),
    "psi": (3.50, 3.86),
    "z": (86.63, 95.75),
}

def find_lifetime_for_mass(mass):
    Lambda = 1000
    ctau = ph.ctaua(mass, 0.5, 0.5, Lambda) # in cm

    boost = 1/mass

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
    
    return boost*ctau

def mass_to_lifetime(input_graph):
    output_graph = TGraphAsymmErrors()
    
    for i in range(input_graph.GetN()):
        mass = input_graph.GetPointX(i)
        x_sec = input_graph.GetPointY(i)
        x_sec_up = input_graph.GetErrorYhigh(i)
        x_sec_down = input_graph.GetErrorYlow(i)
        
        lifetime = find_lifetime_for_mass(mass)
        
        output_graph.SetPoint(i, lifetime, x_sec)
        output_graph.SetPointError(i, 0, 0, x_sec_down, x_sec_up)
        
    return output_graph


def find_coupling_for_cross_section(x_sec, mass):
    couping = x_sec/(-0.0007*mass+0.1218)
    couping = sqrt(couping)
    return couping


def cross_section_to_coupling(input_graph):
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

    
def save_canvas(title, x_title, y_title, theory_line, graph_mean, graph_1sigma, graph_2sigma, is_lifetime=False, is_coupling=False):
    canvas = TCanvas(title, title, 800, 600)
    
    canvas.cd()
    
    gPad.SetLogy()
    gPad.SetLogx()
    
    graph_2sigma.SetFillColor(kYellow)
    graph_2sigma.Draw("A3")
    
    graph_1sigma.SetFillColor(kGreen + 1)
    graph_1sigma.Draw("3")
    
    graph_mean.SetLineStyle(2)
    graph_mean.Draw("L")
    
    if mask_masses and not is_lifetime:
        boxes = []
        y_low = 3e-3 if is_coupling else 3e-5
        y_high = 5e-1 if is_coupling else 1e-2
    
        for low, high in regions_to_mask.values():
            if high > 90:
                high = 88
        
            boxes.append(TBox(low, y_low, high, y_high))
            boxes[-1].Draw()
            boxes[-1].SetFillColor(kWhite)
            boxes[-1].SetLineColor(kWhite)
    
    theory_line.SetLineColor(kRed)
    theory_line.Draw("L")
    
    if is_coupling:
        graph_2sigma.SetMinimum(2e-3)
        graph_2sigma.SetMaximum(1e2)
    else:
        graph_2sigma.SetMinimum(2e-5)
        graph_2sigma.SetMaximum(1e2)
    
    if is_lifetime:
        graph_2sigma.GetXaxis().SetRangeUser(1e-5, 1e5)
        gPad.SetLogx()
    else:
        graph_2sigma.GetXaxis().SetRangeUser(0, 90)
    
    graph_2sigma.GetYaxis().SetTitle(y_title)
    graph_2sigma.GetXaxis().SetTitle(x_title)
    
    legend = TLegend(0.3, 0.7, 0.6, 0.9)
    legend.AddEntry(theory_line, "Theoretical c_{tt}" if is_coupling else "Theoretical #sigma", "l")
    legend.AddEntry(graph_mean, "Median expected", "l")
    legend.AddEntry(graph_1sigma, "68% expected", "f")
    legend.AddEntry(graph_2sigma, "95% expected", "f")
    legend.Draw()
    
    canvas.Update()
    canvas.SaveAs(f"{title}.pdf")





def main():
    file = TFile.Open(input_path)
    
    graph_mean = file.Get("limits_mean")
    graph_1sigma = file.Get("limits_1_sigma")
    graph_2sigma = file.Get("limits_2_sigma")
    
    
    theory_line = TGraph()
    
    i_point = 0
    
    for mass, x_sec in reference_points.items():
        theory_line.SetPoint(i_point, mass, x_sec)
        i_point += 1


    theory_line_lifetime = mass_to_lifetime(theory_line)
    graph_mean_lifetime = mass_to_lifetime(graph_mean)
    graph_1sigma_lifetime = mass_to_lifetime(graph_1sigma)
    graph_2sigma_lifetime = mass_to_lifetime(graph_2sigma)

    theory_line_coupling = cross_section_to_coupling(theory_line)
    graph_mean_coupling = cross_section_to_coupling(graph_mean)
    graph_1sigma_coupling = cross_section_to_coupling(graph_1sigma)
    graph_2sigma_coupling = cross_section_to_coupling(graph_2sigma)

    save_canvas("limits_mass", "m_{a} (GeV)", "#sigma(pp#rightarrow t#bar{t}a) #times BR(a#rightarrow #mu#mu) (pb)",
                theory_line, graph_mean, graph_1sigma, graph_2sigma)

    save_canvas("limits_lifetime", "<#beta#gamma>c#tau (cm)",
                "#sigma(pp#rightarrow t#bar{t}a) #times BR(a#rightarrow #mu#mu) (pb)",
                theory_line_lifetime, graph_mean_lifetime, graph_1sigma_lifetime, graph_2sigma_lifetime,
                is_lifetime=True)

    save_canvas("limits_coupling", "m_{a} (GeV)", "c_{tt}",
                theory_line_coupling, graph_mean_coupling, graph_1sigma_coupling, graph_2sigma_coupling,
                is_lifetime=False, is_coupling=True)
    


if __name__ == "__main__":
    main()
