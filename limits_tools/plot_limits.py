from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, TLegend, TGraphAsymmErrors

import physics as ph

input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-10GeV_mass-cuts_dR-0p2.root"

reference_points = {
    # mass (GeV), x_sec (pb)
    0.1:  3.102,
    0.2: 3.066,
    0.3: 3.075,
    0.315: 3.122,
    0.5: 3.098,
    1.0: 3.104,
    4.0: 3.057,
    8.0: 3.023,
    8.5: 3.086,
    10.: 3.046
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
    
    
def save_canvas(title, x_title, theory_line, graph_mean, graph_1sigma, graph_2sigma, is_lifetime=False):
    canvas = TCanvas(title, title, 800, 600)
    
    canvas.cd()
    
    gPad.SetLogy()
    
    graph_2sigma.SetFillColor(kYellow)
    graph_2sigma.Draw("A3")
    
    graph_1sigma.SetFillColor(kGreen + 1)
    graph_1sigma.Draw("3")
    
    graph_mean.SetLineStyle(2)
    graph_mean.Draw("L")
    
    theory_line.SetLineColor(kRed)
    theory_line.Draw("L")
    
    graph_2sigma.SetMinimum(2e-4)
    graph_2sigma.SetMaximum(1e2)
    
    if is_lifetime:
        graph_2sigma.GetXaxis().SetRangeUser(1e-5, 1e5)
        gPad.SetLogx()
    else:
        graph_2sigma.GetXaxis().SetRangeUser(0, 10)
    
    graph_2sigma.GetYaxis().SetTitle("#sigma(pp#rightarrow t#bar{t}a) #times BR(a#rightarrow #mu#mu) (pb)")
    graph_2sigma.GetXaxis().SetTitle(x_title)
    
    legend = TLegend(0.2, 0.7, 0.5, 0.9)
    legend.AddEntry(theory_line, "Theoretical #sigma", "l")
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


    save_canvas("limits_mass", "m_{a} (GeV)", theory_line, graph_mean, graph_1sigma, graph_2sigma)

    theory_line_lifetime = mass_to_lifetime(theory_line)
    graph_mean_lifetime = mass_to_lifetime(graph_mean)
    graph_1sigma_lifetime = mass_to_lifetime(graph_1sigma)
    graph_2sigma_lifetime = mass_to_lifetime(graph_2sigma)

    save_canvas("limits_lifetime", "<#beta#gamma>c#tau (cm)",
                theory_line_lifetime, graph_mean_lifetime, graph_1sigma_lifetime, graph_2sigma_lifetime,
                is_lifetime=True)


if __name__ == "__main__":
    main()
