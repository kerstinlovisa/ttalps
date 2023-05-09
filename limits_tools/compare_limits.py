from math import sqrt, pi

from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, kViolet, kBlue, TLegend, kCyan, kOrange, kBlack, TF1, kWhite, kPink

from limits_tools import alp_cross_section_only_top_coupling, cross_section_to_coupling


base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/"

limits_variants = [
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default", kBlack, 2, "default"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default_displacedOnly", kGreen+1, 1, "default, l_xy > 200 #mu m"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default_newCuts", kBlack, 1, "default, new cuts"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default_newCuts_firstMin", kRed, 3, "default, new cuts, first"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default_firstMuon", kBlack, 2, "default, first muon"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default_lastMuon", kGreen+1, 3, "default, last muon"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default_trackerOnly", kBlack, 2, "default lifetime, tracker only"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1mm", kViolet, 1, "1 mm"),
    
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e0mm_newCuts", kPink,        1, "1e0 mm, new cuts"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e1mm_newCuts", kViolet,      1, "1e1 mm, new cuts"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e4mm_newCuts", kBlue,        1, "1e4 mm, new cuts"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e5mm_newCuts", kCyan+1,      1, "1e5 mm, new cuts"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e6mm_newCuts", kGreen+1,     1, "1e6 mm, new cuts"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e7mm_newCuts", kOrange+1,    1, "1e7 mm, new cuts"),
    
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e4mm", kBlue, 2, "1e4 mm"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e5mm", kCyan+1, 2, "1e5 mm"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e6mm", kGreen+1, 2, "1e6 mm"),
    ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e7mm", kOrange+1, 2, "1e7 mm"),
    
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e6mm_trackerOnly", kGreen+1, 2, "1e6 mm, tracker only"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-2e6mm", kGreen+1, 2, "2e6 mm"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-3e6mm", kGreen+1, 3, "3e6 mm"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-3e6mm_moreStats", kGreen, 3, "3e6 mm"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-5e6mm", kGreen+1, 1, "5e6 mm"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-5e6mm_ref-1pb_rescaled", kGreen+1, 1, "5e6 mm, 1 pb (rescaled)"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-5e6mm_ref-0p1pb_rescaled", kBlue, 2, "5e6 mm, 0.1 pb (rescaled)"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-5e6mm_ref-0p1pb_nonRescaled", kViolet, 1, "5e6 mm, 0.1 pb (not rescaled)"),
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-8e6mm", kGreen+1, 5, "8e6 mm"),
    
    # ("pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-2e7mm", kOrange+1, 2, "2e7 mm"),
    
    
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
    theory_line.SetLineColor(kWhite)
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
    
    line_1pb = TF1("1pb", "1", 0, 100)
    line_1pb.SetLineColor(kGreen+1)
    line_1pb.SetLineStyle(2)

    line_0p1pb = TF1("1pb", "0.1", 0, 100)
    line_0p1pb.SetLineColor(kViolet)
    line_0p1pb.SetLineStyle(2)
    
    # optimal_graph_5e6mm = TGraph()
    # optimal_graph_5e6mm.SetPoint(0, 0.35, 32.33333333333333)
    # optimal_graph_5e6mm.SetPoint(1, 0.5, 22.222222222222225)
    # optimal_graph_5e6mm.SetPoint(2, 0.9, 8.25)
    # optimal_graph_5e6mm.SetPoint(3, 1.25, 4.166666666666666)
    # optimal_graph_5e6mm.SetPoint(4, 2, 2.6133333333333333)
    # optimal_graph_5e6mm.SetPoint(5, 4, 1.2452830188679245)
    # optimal_graph_5e6mm.SetPoint(6, 8, 0.825)
    # optimal_graph_5e6mm.SetPoint(7, 10, 0.5952380952380953)
    #
    # optimal_graph_5e6mm.SetLineColor(kGreen+1)
    # optimal_graph_5e6mm.SetLineStyle(2)
    # legend.AddEntry(optimal_graph_5e6mm, "10 events at 5e6 mm", "L")
    #
    # optimal_graph_1e5mm = TGraph()
    # optimal_graph_1e5mm.SetPoint(0, 0.35, 0.3010752688172043)
    # optimal_graph_1e5mm.SetPoint(1, 0.5, 0.28860028860028863)
    # optimal_graph_1e5mm.SetPoint(2, 0.9, 0.21221864951768488)
    # optimal_graph_1e5mm.SetPoint(3, 1.25, 0.12865497076023394)
    # optimal_graph_1e5mm.SetPoint(4, 2, 0.09116022099447513)
    # optimal_graph_1e5mm.SetPoint(5, 4, 0.059620596205962065)
    # optimal_graph_1e5mm.SetPoint(6, 8, 0.0316844487552538)
    # optimal_graph_1e5mm.SetPoint(7, 10, 0.01614481409001957)
    #
    # optimal_graph_1e5mm.SetLineColor(kCyan+1)
    # optimal_graph_1e5mm.SetLineStyle(2)
    # legend.AddEntry(optimal_graph_1e5mm, "10 events at 1e5 mm", "L")
    
    canvas_cross_section.cd()
    legend.Draw()
    # line_1pb.Draw("same")
    # line_0p1pb.Draw("same")
    # optimal_graph_5e6mm.Draw("Lsame")
    # optimal_graph_1e5mm.Draw("Lsame")

    canvas_coupling.cd()
    legend.Draw()
    
    canvas_cross_section.Update()
    canvas_cross_section.SaveAs("limits_comparison.pdf")

    canvas_coupling.Update()
    canvas_coupling.SaveAs("limits_comparison_coupling.pdf")

    
    
    
    

if __name__ == "__main__":
    main()