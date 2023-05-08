from numpy import linspace, logspace, array
from math import pi

from ROOT import TFile, TCanvas, gPad, gStyle, TGraph, gROOT, TLatex
from ROOT import kViolet, kBlue, kCyan, kGreen, kOrange, kRed

from limits_tools import find_lifetime_for_mass_mumuonly_noboost

min_ctau_exp = 0
max_ctau_exp = 8

Lambda = 4*pi*1000
coupling = 0.5

def main():
    gStyle.SetLineScalePS(1)
    
    input_file = TFile.Open("lifetime_vs_mass_limits_function.root")
    limits_fun = input_file.Get("limits")
    limits_fun.SetNpy(10000)

    limits_fun_tiny = input_file.Get("limits_tiny")
    limits_fun_tiny.SetNpy(10000)
    
    canvas = TCanvas("canvas", "canvas", 2880, 1800)
    canvas.Divide(2, 2)
    
    canvas.cd(1)
    gPad.SetLogy()
    gPad.SetLogz()

    limits_fun.Draw("colz")
    limits_fun.GetXaxis().SetTitle("m_{a} (GeV)")
    limits_fun.GetYaxis().SetTitle("c#tau (mm)")

    canvas.cd(2)
    gPad.SetLogy()
    gPad.SetLogz()

    limits_fun_tiny.Draw("colz")
    limits_fun_tiny.GetXaxis().SetTitle("m_{a} (GeV)")
    limits_fun_tiny.GetYaxis().SetTitle("c#tau (mm)")
    
    
    isobarns = {
        1.0: [TGraph(), 0, 99999999, 999999999],
        1e-1: [TGraph(), 0, 99999999, 999999999],
        1e-2: [TGraph(), 0, 99999999, 999999999],
        1e-3: [TGraph(), 0, 99999999, 999999999],
        1e-4: [TGraph(), 0, 99999999, 999999999],
        # 1e-5: [TGraph(), 0, 99999999, 999999999],
        # 1e-6: [TGraph(), 0, 99999999, 999999999],
    }

    for mass in linspace(0, 10, 200):
    
        for desired_xsec, _ in isobarns.items():
            isobarns[desired_xsec][2] = 999999999
            isobarns[desired_xsec][3] = 999999999
        
        for ctau in logspace(min_ctau_exp, max_ctau_exp, 1000):
            xsec = limits_fun.Eval(mass, ctau)
            xsec_tiny = limits_fun_tiny.Eval(mass, ctau) / 1e9
            
            for desired_xsec, [_, _, closest_xsec, _] in isobarns.items():
                
                xsec_comp = xsec if desired_xsec >= 1e-2 else xsec_tiny
                
                if abs(desired_xsec - xsec_comp) < abs(desired_xsec-closest_xsec):
                    isobarns[desired_xsec][2] = xsec_comp
                    isobarns[desired_xsec][3] = ctau

        for xsec, (graph, i_point, closest_xsec, closest_ctau) in isobarns.items():
            if closest_ctau > 10**min_ctau_exp and closest_ctau < 10**max_ctau_exp:
                
                plotting_ctau = closest_ctau

                if mass > 8.5 or mass < 0.3:
                    plotting_ctau = 0
                
                graph.SetPoint(i_point, mass, plotting_ctau / 1000)
                isobarns[xsec][1] += 1

    # canvas.cd(1)
    # for xsec, (graph, i_point, closest_xsec, closest_ctau) in isobarns.items():
    #     graph.Draw("Lsame")

    canvas.cd(3)
    gPad.SetLogy()
    
    colors = (kViolet, kBlue, kCyan+1, kGreen+1, kOrange)
    labels = []
    label_texts = ["1 pb", "0.1 pb", "10 fb", "1 fb", "0.1 fb"]
    
    for i_plot, (xsec, (graph, i_point, closest_xsec, closest_ctau)) in enumerate(isobarns.items()):
        
        color = colors[len(colors)-i_plot-1]

        graph.SetLineColor(color)
        graph.SetFillColorAlpha(color, 0.05)
        
        if i_plot == 0:
            graph.Draw("ALF")

            graph.GetXaxis().SetTitle("m_{a} (GeV)")
            graph.GetYaxis().SetTitle("c#tau (m)")

            graph.GetXaxis().SetLimits(0.2, 8.6)

            # graph.SetMinimum(1e-1)
            graph.SetMinimum(1e-7)
            graph.SetMaximum(1e5)
        else:
            graph.Draw("LFsame")

        labels.append(TLatex(7.5, 2*10**(4-i_plot), label_texts[i_plot]))

        labels[i_plot].SetTextColor(color)
        labels[i_plot].SetTextSize(0.04)
        
        labels[i_plot].Draw()

    theory_line = TGraph()
    i_point = 0

    for mass in logspace(-1, 1, 100):
        ctau = find_lifetime_for_mass_mumuonly_noboost(mass, coupling, Lambda)
        ctau /= 1000  # convert from mm to m
        theory_line.SetPoint(i_point, mass, ctau)
        i_point += 1

    theory_line.SetLineColor(kRed)
    theory_line.Draw("same")
    
    canvas.Update()
    canvas.SaveAs("lifetime_vs_mass_isobarns.pdf")


if __name__ == "__main__":
    main()