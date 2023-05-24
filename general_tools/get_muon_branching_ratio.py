from math import pi
from numpy import linspace, logspace

from ROOT import TGraph, TCanvas, kBlack, gPad, kRed

from limits_tools import find_lifetime_for_mass, find_lifetime_for_mass_mumuonly_noboost

Lambda = 4*pi*1000
coupling = 0.5


def main():
    
    graph = TGraph()

    # for i_mass, mass in enumerate(linspace(0.1, 10, 100)):
    for i_mass, mass in enumerate(logspace(-1, 1, 100)):
        gamma_total = find_lifetime_for_mass(mass, coupling, Lambda)
        gamma_mumu = find_lifetime_for_mass_mumuonly_noboost(mass, coupling, Lambda)

        branching_ratio = gamma_total/gamma_mumu

        graph.SetPoint(i_mass, mass, branching_ratio)
        # print(f"{mass}: {branching_ratio}")

    for mass in (0.3, 0.35, 0.5, 0.9, 1.25, 2, 4, 8, 10):
        gamma_total = find_lifetime_for_mass(mass, coupling, Lambda)
        gamma_mumu = find_lifetime_for_mass_mumuonly_noboost(mass, coupling, Lambda)
        branching_ratio = gamma_total/gamma_mumu
        print(f"{mass}: {branching_ratio},")

    canvas = TCanvas("canvas", "canvas", 800, 600)
    canvas.cd()

    gPad.SetLogx()
    gPad.SetLogy()

    graph.SetLineColor(kRed)
    graph.Draw("AL")

    graph.GetXaxis().SetTitle("m_{a} GeV")
    graph.GetYaxis().SetTitle("BR(a#rightarrow#mu#mu)")
    canvas.Update()
    canvas.SaveAs("br_vs_mass.pdf")



if __name__ == "__main__":
    main()