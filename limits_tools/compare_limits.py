from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, kViolet, kBlue, TLegend, kCyan, kOrange


limits_variants = [
    ("mass-cuts", kViolet, 1, "mass cuts"),
    ("pt-5GeV_mass-cuts", kBlue, 1, "mass cuts, p_{T, #mu} > 5 GeV"),
    ("pt-10GeV_mass-cuts", kBlue, 2, "mass cuts, p_{T, #mu} > 10 GeV"),
    ("pt-10GeV_mass-cuts_dR-0p1", kGreen+1, 2, "mass cuts, p_{T, #mu} > 10 GeV, #Delta R < 0.1"),
    ("pt-10GeV_mass-cuts_dR-0p2", kGreen+1, 1, "mass cuts, p_{T, #mu} > 10 GeV, #Delta R < 0.2"),
    ("pt-5GeV_mass-cuts_dR-0p2", kOrange, 1, "mass cuts, p_{T, #mu} > 5 GeV, #Delta R < 0.2"),
]

base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/"

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

theory_line = TGraph()

i_point = 0

for mass, x_sec in reference_points.items():
    theory_line.SetPoint(i_point, mass, x_sec)
    i_point += 1

canvas = TCanvas("limits", "limits", 800, 600)

canvas.cd()

gPad.SetLogy()

theory_line.SetLineColor(kRed)
theory_line.Draw("AL")

theory_line.SetMinimum(2e-4)
theory_line.SetMaximum(2e3)
theory_line.GetXaxis().SetRangeUser(0, 10)

theory_line.GetYaxis().SetTitle("#sigma(pp#rightarrow t#bar{t}a) #times BR(a#rightarrow #mu#mu) (pb)")
theory_line.GetXaxis().SetTitle("m_{a} (GeV)")


legend = TLegend(0.15, 0.6, 0.7, 0.9)

files = {}

legend.AddEntry(theory_line, "theory", "l")

for (cuts, color, style, title) in limits_variants:
    files[cuts] = TFile.Open(f"{base_path}limits_{cuts}.root")
    graph_mean = files[cuts].Get("limits_mean")
    graph_mean.SetLineColor(color)
    graph_mean.SetLineStyle(style)
    graph_mean.Draw("Lsame")
    
    legend.AddEntry(graph_mean, title, "l")

dummy_graph = TGraph()
legend.AddEntry(dummy_graph, "", "")

legend.Draw()

canvas.Update()
canvas.SaveAs("limits_comparison.pdf")
