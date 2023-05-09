from numpy import linspace, logspace, array
from math import pi

from ROOT import TFile, TCanvas, gPad, gStyle, TGraph, gROOT, TLatex
from ROOT import kViolet, kBlue, kCyan, kGreen, kOrange, kRed

from limits_tools import find_lifetime_for_mass_mumuonly_noboost

# ----------------------------------------------------------------------------------------------------------------------
# Options

input_file_name = "lifetime_vs_mass_limits_function.root"

isobarns_to_draw = (1e0, 1e-1, 1e-2, 1e-3, 1e-4)
label_texts = ["1 pb", "0.1 pb", "10 fb", "1 fb", "0.1 fb"]
colors = (kOrange, kGreen+1, kCyan+1, kBlue, kViolet)

min_c_tau_exp = 0
max_c_tau_exp = 8

Lambda = 4*pi*1000
coupling = 0.5

use_tiny_below = 1e-2

#
# ----------------------------------------------------------------------------------------------------------------------


def get_isobarns(limits_fun, limits_fun_tiny):
    isobarns = {xsec: [TGraph(), 0, 99999999, 999999999] for xsec in isobarns_to_draw}
    
    for mass in linspace(0, 10, 200):
        
        for desired_xsec, _ in isobarns.items():
            isobarns[desired_xsec][2] = 999999999
            isobarns[desired_xsec][3] = 999999999
        
        for c_tau in logspace(min_c_tau_exp, max_c_tau_exp, 1000):
            xsec = limits_fun.Eval(mass, c_tau)
            
            xsec_tiny = limits_fun_tiny.Eval(mass, c_tau) / 1e9
            
            for desired_xsec, [_, _, closest_xsec, _] in isobarns.items():
                
                xsec_comp = xsec if desired_xsec >= use_tiny_below else xsec_tiny
                
                if abs(desired_xsec - xsec_comp) < abs(desired_xsec - closest_xsec):
                    isobarns[desired_xsec][2] = xsec_comp
                    isobarns[desired_xsec][3] = c_tau
        
        for xsec, (graph, i_point, closest_xsec, closest_c_tau) in isobarns.items():
            if 10 ** min_c_tau_exp < closest_c_tau < 10 ** max_c_tau_exp:
                
                plotting_c_tau = closest_c_tau
                
                if mass > 8.5 or mass < 0.3:
                    plotting_c_tau = 0
                
                graph.SetPoint(i_point, mass, plotting_c_tau / 1000)  # mm -> m
                isobarns[xsec][1] += 1
    
    isobarns = {xsec: params[0] for xsec, params in isobarns.items()}
    
    return isobarns


def get_theory_line():
    theory_line = TGraph()
    theory_line.SetLineColor(kRed)
    i_point = 0

    for mass in logspace(-1, 1, 100):
        c_tau = find_lifetime_for_mass_mumuonly_noboost(mass, coupling, Lambda)
        c_tau /= 1000  # convert from mm to m
        theory_line.SetPoint(i_point, mass, c_tau)
        i_point += 1
        
    return theory_line


def draw_isobarns(isobarns):
    for i_plot, (_, graph) in enumerate(isobarns.items()):
        graph.Draw("ALF" if i_plot == 0 else "LFsame")

        graph.SetLineColor(colors[i_plot])
        graph.SetFillColorAlpha(colors[i_plot], 0.05)
        graph.GetXaxis().SetTitle("m_{a} (GeV)")
        graph.GetYaxis().SetTitle("c#tau (m)")
        graph.GetXaxis().SetLimits(0.2, 8.6)
        # graph.SetMinimum(1e-1)
        graph.SetMinimum(1e-7)
        graph.SetMaximum(1e5)

        label = TLatex(7.5, 2*10**(4-i_plot), label_texts[i_plot])
        label.SetTextColor(colors[i_plot])
        label.SetTextSize(0.04)
        label.DrawClone()


def get_limit_functions():
    input_file = TFile.Open(input_file_name)
    limits_fun = input_file.Get("limits")
    limits_fun.SetNpy(10000)

    limits_fun_tiny = input_file.Get("limits_tiny")
    limits_fun_tiny.SetNpy(10000)
    
    return limits_fun, limits_fun_tiny


def main():
    gStyle.SetLineScalePS(1)
    
    canvas_2d_functions = TCanvas("canvas_2d_functions", "canvas_2d_functions", 1600, 600)
    canvas_2d_functions.Divide(2, 1)

    canvas_2d_functions.cd(1)
    gPad.SetLogy()
    gPad.SetLogz()

    limits_fun, limits_fun_tiny = get_limit_functions()
    limits_fun.Draw("colz")
    limits_fun.GetXaxis().SetTitle("m_{a} (GeV)")
    limits_fun.GetYaxis().SetTitle("c#tau (mm)")

    canvas_2d_functions.cd(2)
    gPad.SetLogy()
    gPad.SetLogz()

    limits_fun_tiny.Draw("colz")
    limits_fun_tiny.GetXaxis().SetTitle("m_{a} (GeV)")
    limits_fun_tiny.GetYaxis().SetTitle("c#tau (mm)")

    canvas_2d_functions.Update()
    canvas_2d_functions.SaveAs("lifetime_vs_mass_2d_functions.pdf")

    canvas_isobarns = TCanvas("canvas_isobarns", "canvas_isobarns", 800, 600)
    canvas_isobarns.cd()
    gPad.SetLogy()

    isobarns = get_isobarns(limits_fun, limits_fun_tiny)
    draw_isobarns(isobarns)
    
    theory_line = get_theory_line()
    theory_line.Draw("same")
    
    canvas_isobarns.Update()
    canvas_isobarns.SaveAs("limit_isobarns.pdf")


if __name__ == "__main__":
    main()
