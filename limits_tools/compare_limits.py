from math import sqrt, pi

from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, kViolet, kBlue, TLegend, kCyan, kOrange

from limits_tools import alp_cross_section_only_top_coupling, cross_section_to_coupling


base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/"

limits_variants = [
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1", kViolet+1, 1, "default_lifetime"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_ctau-1e5mm", kCyan+1, 1, "1e5 mm"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_ctau-1e2mm", kBlue, 1, "100 mm"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_ctau-1mm", kGreen+1, 1, "1 mm"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_ctau-1em4mm", kOrange, 1, "1e-4 mm"),
]


def main():
    
    theory_line = TGraph()
    
    i_point = 0
    
    for mass, x_sec in alp_cross_section_only_top_coupling.items():
        theory_line.SetPoint(i_point, mass, x_sec)
        i_point += 1
    
    canvas_cross_section = TCanvas("limits_x_sec", "limits_x_sec", 800, 600)
    canvas_coupling = TCanvas("limits_coupling", "limits_coupling", 800, 600)
    
    canvas_cross_section.cd()
    
    gPad.SetLogy()
    # gPad.SetLogx()
    
    theory_line.SetLineColor(kRed)
    theory_line.Draw("AL")
    
    theory_line.SetMinimum(2e-5)
    theory_line.SetMaximum(2e3)
    theory_line.GetXaxis().SetRangeUser(0.3, 10)
    
    theory_line.GetYaxis().SetTitle("#sigma(pp#rightarrow t#bar{t}a) #times BR(a#rightarrow #mu#mu) (pb)")
    theory_line.GetXaxis().SetTitle("m_{a} (GeV)")
    
    canvas_coupling.cd()
    gPad.SetLogy()
    # gPad.SetLogx()

    theory_line_coupling = cross_section_to_coupling(theory_line)

    theory_line_coupling.SetMinimum(1e-2)
    theory_line_coupling.SetMaximum(1e2)
    theory_line_coupling.GetXaxis().SetRangeUser(0.3, 10)

    theory_line_coupling.GetYaxis().SetTitle("c_{tt}")
    theory_line_coupling.GetXaxis().SetTitle("m_{a} (GeV)")

    theory_line_coupling.SetLineColor(kRed)
    theory_line_coupling.Draw("AL")
    
    legend = TLegend(0.3, 0.7, 0.7, 0.9)
    
    files = {}
    
    legend.AddEntry(theory_line, "theory", "l")
    
    for (cuts, color, style, title) in limits_variants:
        files[cuts] = TFile.Open(f"{base_path}limits_{cuts}.root")
        graph_mean = files[cuts].Get("limits_mean")
        graph_mean.SetLineColor(color)
        graph_mean.SetLineStyle(style)

        canvas_cross_section.cd()
        graph_mean.Draw("Lsame")

        canvas_coupling.cd()
        graph_mean_coupling = cross_section_to_coupling(graph_mean)
        graph_mean_coupling.SetLineColor(color)
        graph_mean_coupling.SetLineStyle(style)
        graph_mean_coupling.DrawClone("Lsame")
        
        legend.AddEntry(graph_mean, title, "l")
    
    dummy_graph = TGraph()
    legend.AddEntry(dummy_graph, "", "")
    
    canvas_cross_section.cd()
    legend.Draw()

    canvas_coupling.cd()
    legend.Draw()
    
    canvas_cross_section.Update()
    canvas_cross_section.SaveAs("limits_comparison.pdf")

    canvas_coupling.Update()
    canvas_coupling.SaveAs("limits_comparison_coupling.pdf")

    
    
    
    

if __name__ == "__main__":
    main()