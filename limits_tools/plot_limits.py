from ROOT import TFile, kGreen, kYellow, TCanvas, gPad


input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits.root"

file = TFile.Open(input_path)

graph_mean = file.Get("limits_mean")
graph_1sigma = file.Get("limits_1_sigma")
graph_2sigma = file.Get("limits_2_sigma")




canvas = TCanvas("limits", "limits", 800, 600)

canvas.cd()

gPad.SetLogy()

graph_2sigma.SetFillColor(kYellow)
graph_2sigma.Draw("A3")

graph_1sigma.SetFillColor(kGreen+1)
graph_1sigma.Draw("3")

graph_mean.SetLineStyle(2)
graph_mean.Draw("L")

graph_2sigma.SetMinimum(1e-3)
graph_2sigma.SetMaximum(1e4)
graph_2sigma.GetXaxis().SetRangeUser(0, 11);

graph_2sigma.GetYaxis().SetTitle("#sigma(a#rightarrow#mu#mu) (fb)")
graph_2sigma.GetXaxis().SetTitle("m_{a} (GeV)")

canvas.Update()
canvas.SaveAs("limits.pdf")