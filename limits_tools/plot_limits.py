from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, TLegend


input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-10GeV_mass-cuts_dR-0p2.root"

file = TFile.Open(input_path)

graph_mean = file.Get("limits_mean")
graph_1sigma = file.Get("limits_1_sigma")
graph_2sigma = file.Get("limits_2_sigma")


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

graph_2sigma.SetFillColor(kYellow)
graph_2sigma.Draw("A3")

graph_1sigma.SetFillColor(kGreen+1)
graph_1sigma.Draw("3")

graph_mean.SetLineStyle(2)
graph_mean.Draw("L")

theory_line.SetLineColor(kRed)
theory_line.Draw("L")

graph_2sigma.SetMinimum(2e-4)
graph_2sigma.SetMaximum(1e2)
graph_2sigma.GetXaxis().SetRangeUser(0, 10)

graph_2sigma.GetYaxis().SetTitle("#sigma(pp#rightarrow t#bar{t}a) #times #Gamma(a#rightarrow #mu#mu) (pb)")
graph_2sigma.GetXaxis().SetTitle("m_{a} (GeV)")


legend = TLegend(0.2, 0.7, 0.5, 0.9)
legend.AddEntry(theory_line, "Theoretical #sigma", "l")
legend.AddEntry(graph_mean, "Median expected", "l")
legend.AddEntry(graph_1sigma, "68% expected", "f")
legend.AddEntry(graph_2sigma, "95% expected", "f")
legend.Draw()

canvas.Update()
canvas.SaveAs("limits.pdf")