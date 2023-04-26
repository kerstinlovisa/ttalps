from math import sqrt, pi

from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, TLegend, TGraphAsymmErrors, TBox, kWhite

import physics as ph
from limits_tools import alp_cross_section_only_top_coupling, mass_to_lifetime, cross_section_to_coupling, regions_to_mask

input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1.root"
mask_masses = True

Lambda = 4*pi*1000
coupling = 0.5


def save_canvas(title, x_title, y_title, theory_line, graph_mean, graph_1sigma, graph_2sigma, is_lifetime=False, is_coupling=False):
    canvas = TCanvas(title, title, 800, 600)
    
    canvas.cd()
    
    graph_2sigma.SetFillColor(kYellow)
    graph_2sigma.Draw("A3")
    
    graph_1sigma.SetFillColor(kGreen + 1)
    graph_1sigma.Draw("3same")
    
    graph_mean.SetLineStyle(2)
    graph_mean.Draw("Lsame")
    
    if mask_masses and not is_lifetime:
        boxes = []
        y_low = 3e-3 if is_coupling else 3e-5
        y_high = 5e-1 if is_coupling else 1e-2
    
        for low, high in regions_to_mask.values():
            if high > 90:
                high = 87
        
            boxes.append(TBox(low, y_low, high, y_high))
            boxes[-1].Draw()
            boxes[-1].SetFillColor(kWhite)
            boxes[-1].SetLineColor(kWhite)
    
    theory_line.SetLineColor(kRed)
    theory_line.Draw("Lsame")

    if is_coupling:
        graph_2sigma.SetMinimum(2e-3)
        graph_2sigma.SetMaximum(1e2)
    else:
        graph_2sigma.SetMinimum(2e-7)
        graph_2sigma.SetMaximum(1e2)
    
    if is_lifetime:
        graph_2sigma.GetXaxis().SetLimits(1e-4, 20)
    else:
        graph_2sigma.GetXaxis().SetRangeUser(0, 90)

    gPad.SetLogy()
    gPad.SetLogx()
    
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
    
    for mass, x_sec in alp_cross_section_only_top_coupling.items():
        theory_line.SetPoint(i_point, mass, x_sec)
        i_point += 1


    theory_line_lifetime = mass_to_lifetime(theory_line, coupling, Lambda)
    graph_mean_lifetime = mass_to_lifetime(graph_mean, coupling, Lambda)
    graph_1sigma_lifetime = mass_to_lifetime(graph_1sigma, coupling, Lambda)
    graph_2sigma_lifetime = mass_to_lifetime(graph_2sigma, coupling, Lambda)

    theory_line_coupling = cross_section_to_coupling(theory_line, coupling)
    graph_mean_coupling = cross_section_to_coupling(graph_mean, coupling)
    graph_1sigma_coupling = cross_section_to_coupling(graph_1sigma, coupling)
    graph_2sigma_coupling = cross_section_to_coupling(graph_2sigma, coupling)

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
