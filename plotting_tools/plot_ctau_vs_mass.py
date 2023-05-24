from numpy import linspace, logspace
from math import pi

from ROOT import TGraph, TCanvas, gPad, TLegend, TLine, TColor
from ROOT import kSpring, kViolet, kBlue, kCyan, kGreen, kOrange, kRed, kBlack, kMagenta

from limits_tools import find_lifetime_for_mass

color_palette_wong = (
    TColor.GetColor(230, 159, 0),
    TColor.GetColor(86, 180, 233),
    TColor.GetColor(0, 158, 115),
    TColor.GetColor(0, 114, 178),
    TColor.GetColor(213, 94, 0),
)

mass_benchmarks = (
    (0.35,  color_palette_wong[0],  1),
    (0.5,   color_palette_wong[0],  2),
    (0.9,   color_palette_wong[2],  1),
    (1.25,  color_palette_wong[2],  2),
    (2,     color_palette_wong[3],  1),
    (4,     color_palette_wong[3],  2),
    (8,     color_palette_wong[4],  1),
)


def main():
    Lambda = 4 * pi * 1000
    
    graphs = {}
    
    for coupling in (0.005, 0.5):
        graphs[coupling] = TGraph()
        
        for i_point, mass in enumerate(logspace(-4, 1, 1000)):
            c_tau = find_lifetime_for_mass(mass, coupling, Lambda, boost = False)
            c_tau /= 1000  # mm -> m
            
            graphs[coupling].SetPoint(i_point, mass, c_tau)
        
    canvas = TCanvas("canvas", "canvas", 800, 600)
    canvas.cd()
    
    gPad.SetLeftMargin(0.18)
    gPad.SetBottomMargin(0.25)

    gPad.SetLogx()
    gPad.SetLogy()
    
    graphs[0.005].SetLineColor(kBlack)
    graphs[0.005].SetLineStyle(2)
    graphs[0.005].SetLineWidth(2)
    graphs[0.005].Draw("AL")

    graphs[0.005].GetXaxis().SetTitle("m_{a} [GeV]")
    graphs[0.005].GetYaxis().SetTitle("c#tau [m]")

    graphs[0.005].GetYaxis().SetNdivisions(5)

    graphs[0.005].GetXaxis().SetLabelSize(0.05)
    graphs[0.005].GetXaxis().SetTitleOffset(1.2)
    graphs[0.005].GetXaxis().SetTitleSize(0.06)
    graphs[0.005].GetXaxis().SetTitleFont(42)
    graphs[0.005].GetXaxis().SetLabelFont(42)

    graphs[0.005].GetYaxis().SetLabelSize(0.05)
    graphs[0.005].GetYaxis().SetTitleOffset(1.2)
    graphs[0.005].GetYaxis().SetTitleSize(0.06)
    graphs[0.005].GetYaxis().SetTitleFont(42)
    graphs[0.005].GetYaxis().SetLabelFont(42)

    graphs[0.005].SetMinimum(1e-11)
    graphs[0.005].SetMaximum(9e5)
    graphs[0.005].GetXaxis().SetLimits(1e-1, 10)

    graphs[0.5].SetLineColor(kBlack)
    graphs[0.5].SetLineStyle(1)
    graphs[0.5].SetLineWidth(2)
    graphs[0.5].Draw("Lsame")
    
    for mass, color, line_style in mass_benchmarks:
        line = TLine(mass, 1e-11, mass, 1e6)
        line.SetLineColor(color)
        line.SetLineStyle(line_style)
        line.SetLineWidth(2)
        line.DrawClone()

    legend = TLegend(0.5, 0.7, 0.9, 0.9)
    legend.AddEntry(graphs[0.005], "c_{tt}/f_{a} = 0.01 / TeV ", "l")
    legend.AddEntry(graphs[0.5], "c_{tt}/f_{a} = 1.00 / TeV ", "l")

    legend.Draw()
    
    canvas.Update()
    canvas.SaveAs("c_tau_vs_mass.pdf")
    

if __name__ == "__main__":
    main()