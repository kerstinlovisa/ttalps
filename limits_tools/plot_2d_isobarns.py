from numpy import linspace, logspace, array
from math import pi

from ROOT import TFile, TCanvas, gPad, gStyle, TGraph, gROOT, TLatex, TGaxis, TColor
from ROOT import kViolet, kBlue, kCyan, kGreen, kOrange, kRed, kBlack, kSpring, kMagenta

from limits_tools import find_lifetime_for_mass_mumuonly_noboost, tiny_scale, large_scale

# ----------------------------------------------------------------------------------------------------------------------
# Options

input_file_name = "lifetime_vs_mass_limits_function.root"

color_palette_wong = (
    TColor.GetColor(230, 159, 0),
    TColor.GetColor(86, 180, 233),
    TColor.GetColor(0, 158, 115),
    TColor.GetColor(0, 114, 178),
    TColor.GetColor(213, 94, 0),
)

color_palette_ibm = (
    TColor.GetColor(100, 143, 255),
    TColor.GetColor(120, 94, 240),
    TColor.GetColor(220, 38, 127),
    TColor.GetColor(254, 97, 0),
    TColor.GetColor(255, 176, 0),
)

color_palette_tol = (
    TColor.GetColor(51, 34, 136),  #
    TColor.GetColor(17, 119, 51),  #
    TColor.GetColor(68, 170, 153),  #
    TColor.GetColor(136, 204, 238),
    TColor.GetColor(221, 204, 119),
    TColor.GetColor(204, 102, 119), #
    TColor.GetColor(170, 69, 153), #
    TColor.GetColor(136, 34, 85),
)

isobarn_params = {
    #                                       label_y
    1e0:    ("1 pb",    color_palette_wong[0],   1.0*10**4),
    1e-1:   ("0.1 pb",  color_palette_wong[1],   2.0*10**3),
    1e-2:   ("10 fb",   color_palette_wong[2],   2.2*10**2),
    1e-3:   ("1 fb",    color_palette_wong[3],   2.2*10**1),
    1e-4:   ("0.1 fb",  color_palette_wong[4],   2.3*10**0),
    # 1e-5:   ("10 ab",   kRed,       2.3*10**-1),
    # 1e-6:   ("1 ab",    kBlack,     2.3*10**-2),
    # 1e-7:   ("0.1 ab",  kOrange+1,  2.3*10**-3),
    # 1e-8:   ("10 zb",   kGreen+1,   2.3*10**-4),
    # 1e-9:   ("1 zb",    kCyan+1,    2.3*10**-5),
}

draw_theory_line = False

min_x = 0
max_x = 8.4

min_y = 1e-6 if draw_theory_line else 3e-2
max_y = 3e4

min_c_tau_exp = 0
max_c_tau_exp = 10

min_c_tau_exp_low = -8
max_c_tau_exp_low = -3

Lambda = 4*pi*1000
coupling = 0.5

use_tiny_below = 1e-9
use_large_above = 1e-9

mass_n_points = 100
c_tau_n_points = 1000

labels_size = 0.05
labels_x = 7

#
# ----------------------------------------------------------------------------------------------------------------------


def get_cross_sections(limits_fun, limits_fun_tiny, limits_fun_large, mass, c_tau):
    xsec = limits_fun.Eval(mass, c_tau)
    xsec_tiny = limits_fun_tiny.Eval(mass, c_tau) / tiny_scale
    xsec_large = limits_fun_large.Eval(mass, c_tau) / large_scale

    return xsec, xsec_tiny, xsec_large


def get_cross_section(xsecs, desired_xsec):
    xsec, xsec_tiny, xsec_large = xsecs
    xsec_comp = xsec

    if desired_xsec < use_tiny_below:
        xsec_comp = xsec_tiny
    if desired_xsec > use_large_above:
        xsec_comp = xsec_large

    return xsec_comp


def fill_graphs(isobarns, mass, low = False):
    min_c_tau = min_c_tau_exp_low if low else min_c_tau_exp
    max_c_tau = max_c_tau_exp_low if low else max_c_tau_exp
    
    for xsec, (graph, i_point, closest_xsec, closest_c_tau) in isobarns.items():
        if 10 ** min_c_tau < closest_c_tau < 10 ** max_c_tau:
            plotting_c_tau = closest_c_tau

            if mass > 8.5 or mass < 0.3:
                plotting_c_tau = 0

            graph.SetPoint(i_point, mass, plotting_c_tau / 1000)  # mm -> m
            isobarns[xsec][1] += 1


def get_isobarns(limits_fun, limits_fun_tiny, limits_fun_large):
    isobarns = {xsec: [TGraph(), 0, 99999999, 999999999] for xsec in isobarn_params.keys()}
    isobarns_low = {xsec: [TGraph(), 0, 99999999, 999999999] for xsec in isobarn_params.keys()}
    
    for mass in linspace(0, 10, mass_n_points):
        
        for desired_xsec, _ in isobarns.items():
            isobarns[desired_xsec][2] = 999999999
            isobarns[desired_xsec][3] = 999999999
        
        for c_tau in logspace(min_c_tau_exp, max_c_tau_exp, c_tau_n_points):
            xsecs = get_cross_sections(limits_fun, limits_fun_tiny, limits_fun_large, mass, c_tau)
            
            for desired_xsec, [_, _, closest_xsec, _] in isobarns.items():
                xsec = get_cross_section(xsecs, desired_xsec)
                
                if abs(desired_xsec - xsec) < abs(desired_xsec - closest_xsec):
                    isobarns[desired_xsec][2] = xsec
                    isobarns[desired_xsec][3] = c_tau

        for c_tau in logspace(min_c_tau_exp_low, max_c_tau_exp_low, c_tau_n_points):
            xsecs = get_cross_sections(limits_fun, limits_fun_tiny, limits_fun_large, mass, c_tau)
            
            # print(f"{mass=}, {c_tau=}")
            
            for desired_xsec, [_, _, closest_xsec, _] in isobarns_low.items():
                # xsec = get_cross_section(xsecs, desired_xsec)
                xsec = xsecs[1]
        
                # print(f"{desired_xsec=}, {xsec=}")
        
                if abs(desired_xsec - xsec) < abs(desired_xsec - closest_xsec):
                    isobarns_low[desired_xsec][2] = xsec
                    isobarns_low[desired_xsec][3] = c_tau
        
        fill_graphs(isobarns, mass)
        fill_graphs(isobarns_low, mass)
    
    isobarns = {xsec: params[0] for xsec, params in isobarns.items()}
    isobarns_low = {xsec: params[0] for xsec, params in isobarns_low.items()}
    
    return isobarns, isobarns_low


def get_theory_line():
    theory_line = TGraph()
    theory_line.SetLineColor(kRed)
    i_point = 0

    for mass in logspace(-1, 1, mass_n_points):
        c_tau = find_lifetime_for_mass_mumuonly_noboost(mass, coupling, Lambda)
        c_tau /= 1000  # convert from mm to m
        theory_line.SetPoint(i_point, mass, c_tau)
        i_point += 1
        
    return theory_line


def draw_isobarns(isobarns, low=False):
    
    gPad.SetLeftMargin(0.15)
    gPad.SetRightMargin(0.15)
    gPad.SetBottomMargin(0.15)
    
    first = True
    
    for xsec, graph in isobarns.items():
        
        plot_options = "LFsame"
        if first and not low:
            plot_options = "ALF"
        if low:
            plot_options = "Lsame"
        
        graph.Draw(plot_options)

        graph.SetLineColor(isobarn_params[xsec][1])
        graph.SetLineWidth(7)
        graph.SetFillColorAlpha(isobarn_params[xsec][1], 0.05)
        
        graph.GetXaxis().SetTitle("m_{a} [GeV]")
        graph.GetYaxis().SetTitle("c#tau [m], L = 150 fb^{-1}")
        graph.GetXaxis().SetLimits(min_x, max_x)

        graph.GetXaxis().SetLabelSize(0.06)
        graph.GetXaxis().SetTitleOffset(1.1)
        graph.GetXaxis().SetTitleSize(0.06)

        graph.GetYaxis().SetLabelSize(0.06)
        graph.GetYaxis().SetTitleOffset(1.1)
        graph.GetYaxis().SetTitleSize(0.06)
        
        graph.SetMinimum(min_y)
        graph.SetMaximum(max_y)

        label = TLatex(labels_x, isobarn_params[xsec][2], isobarn_params[xsec][0])
        label.SetTextColor(isobarn_params[xsec][1])
        label.SetTextSize(labels_size)
        label.SetTextFont(42)
        label.DrawClone()
        
        first = False

    axis = TGaxis(max_x, min_y, max_x, max_y, min_y*20, max_y*20, 510, "GL+")
    axis.SetTitle("c#tau [m], L = 3 ab^{-1}")
    axis.SetLineColor(color_palette_wong[3])
    axis.SetLabelColor(color_palette_wong[3])
    axis.SetTitleColor(color_palette_wong[3])

    axis.SetLabelSize(0.06)
    axis.SetTitleOffset(1.1)
    axis.SetTitleSize(0.06)
    
    axis.SetLabelFont(42)
    axis.SetTitleFont(42)
    axis.DrawClone()

    text = TLatex(0.63, 0.91, "#sqrt{s} = 13 TeV")
    text.SetNDC(True)
    text.SetTextSize(0.06)
    text.SetTextFont(42)
    text.DrawClone()


def get_limit_functions():
    input_file = TFile.Open(input_file_name)
    limits_fun = input_file.Get("limits")
    limits_fun.SetNpy(10000)

    limits_fun_tiny = input_file.Get("limits_tiny")
    limits_fun_tiny.SetNpy(10000)

    limits_fun_large = input_file.Get("limits_large")
    limits_fun_large.SetNpy(10000)
    
    return limits_fun, limits_fun_tiny, limits_fun_large


def main():
    gStyle.SetLineScalePS(1)
    
    canvas_2d_functions = TCanvas("canvas_2d_functions", "canvas_2d_functions", 2400, 600)
    canvas_2d_functions.Divide(3, 1)

    canvas_2d_functions.cd(1)
    gPad.SetLogy()
    gPad.SetLogz()

    limits_fun, limits_fun_tiny, limits_fun_large = get_limit_functions()
    limits_fun.Draw("colz")
    limits_fun.GetXaxis().SetTitle("m_{a} (GeV)")
    limits_fun.GetYaxis().SetTitle("c#tau (mm)")

    canvas_2d_functions.cd(2)
    gPad.SetLogy()
    gPad.SetLogz()

    limits_fun_tiny.Draw("colz")
    limits_fun_tiny.GetXaxis().SetTitle("m_{a} (GeV)")
    limits_fun_tiny.GetYaxis().SetTitle("c#tau (mm)")

    canvas_2d_functions.cd(3)
    gPad.SetLogy()
    gPad.SetLogz()

    limits_fun_large.Draw("colz")
    limits_fun_large.GetXaxis().SetTitle("m_{a} (GeV)")
    limits_fun_large.GetYaxis().SetTitle("c#tau (mm)")

    canvas_2d_functions.Update()
    canvas_2d_functions.SaveAs("lifetime_vs_mass_2d_functions.pdf")

    canvas_isobarns = TCanvas("canvas_isobarns", "canvas_isobarns", 800, 600)
    canvas_isobarns.cd()
    gPad.SetLogy()

    isobarns, isobarns_low = get_isobarns(limits_fun, limits_fun_tiny, limits_fun_large)
    draw_isobarns(isobarns)
    # draw_isobarns(isobarns_low, low=True)
    
    if draw_theory_line:
        theory_line = get_theory_line()
        theory_line.Draw("same")
    
    canvas_isobarns.Update()
    canvas_isobarns.SaveAs("limit_isobarns.pdf")


if __name__ == "__main__":
    main()
