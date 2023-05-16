from math import sqrt, pi
from numpy import logspace

from ROOT import TFile, TCanvas, gPad, TGraph, TLegend, TGraphAsymmErrors, TBox, TF1, TLatex, gStyle, gROOT, TColor, TArrow
from ROOT import kGreen, kYellow, kRed, kWhite, kViolet, kBlack

import physics as ph
from limits_tools import alp_cross_section_only_top_coupling, mass_to_lifetime, cross_section_to_coupling, regions_to_mask, find_lifetime_for_mass

# input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-2e7mm.root"
# input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default.root"
input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default_newCuts.root"
# input_path = "limits_ctau_vs_mass.root"

mask_masses = True
ctau_limits = False
draw_1pb_line = False

Lambda = 4*pi*1000
coupling = 0.5

max_x = 10

color_palette_wong = (
    TColor.GetColor(230, 159, 0),  # orange
    TColor.GetColor(86, 180, 233),  # light blue
    TColor.GetColor(0, 158, 115),  # green
    TColor.GetColor(0, 114, 178),  # dark blue
    TColor.GetColor(213, 94, 0),  # red
    TColor.GetColor(240, 228, 66),  # yellow
    TColor.GetColor(204, 121, 167),  # pink
)


# default colors
# run2_expected_color = kBlack
# run2_1sigma_color = kGreen+1
# run2_2sigma_color = kYellow
# hllhc_expected_color = kViolet
# theory_color = kRed

# wong colors
run2_expected_color = kBlack
run2_1sigma_color = color_palette_wong[2]
run2_2sigma_color = color_palette_wong[5]
hllhc_expected_color = color_palette_wong[6]
theory_color = color_palette_wong[0]


canvases = {
    "coupling_vs_mass": TCanvas("coupling_vs_mass", "coupling_vs_mass", 800, 600),
    "mass_vs_lifetime": TCanvas("mass_vs_lifetime", "mass_vs_lifetime", 800, 600),
    "xsec_vs_lifetime": TCanvas("xsec_vs_lifetime", "xsec_vs_lifetime", 800, 600),
    "xsec_vs_mass": TCanvas("xsec_vs_mass", "xsec_vs_mass", 800, 600),
    "xsec_and_coupling": TCanvas("xsec_and_coupling", "xsec_and_coupling", 800, 600),
}


def convert_mm_to_m(graph):
    output_graph = TGraphAsymmErrors()
    
    for i_point in range(graph.GetN()):
        x = graph.GetPointX(i_point)
        y = graph.GetPointY(i_point)
        
        x_up = graph.GetErrorXhigh(i_point)
        x_down = graph.GetErrorXlow(i_point)
        y_up = graph.GetErrorYhigh(i_point)
        y_down = graph.GetErrorYlow(i_point)
        
        output_graph.SetPoint(i_point, x/1000, y)
        output_graph.SetPointError(i_point, x_down/1000, x_up/1000, y_down, y_up)
    
    return output_graph


def get_lumi_label(mode):
    if mode == "mass_vs_lifetime":
        text = TLatex(0.6, 0.91, "L = 150 fb^{-1}, #sqrt{s} = 13 TeV")
        text.SetNDC(True)
    elif mode == "xsec_vs_mass" or "coupling_vs_mass":
        text = TLatex(0.68, 0.91, "#sqrt{s} = 13 TeV")
        text.SetNDC(True)
        text.SetTextSize(0.06)
    else:
        # text = TLatex(0.34, 0.74, "L = 150 fb^{-1}, #sqrt{s} = 13 TeV")
        text = TLatex(0.42, 0.74, "#sqrt{s} = 13 TeV")
        text.SetNDC(True)
        text.SetTextSize(0.10)
        
    text.SetTextFont(42)
    text.SetNDC(True)
    
    gStyle.SetStatStyle(0)
    gStyle.SetTitleStyle(0)
    gROOT.ForceStyle()
    return text


def prepare_2sigma_graph(graph, x_title, y_title, mode):
    graph.SetFillColor(run2_2sigma_color)
    
    graph.GetXaxis().SetTitle(x_title)
    graph.GetYaxis().SetTitle(y_title)

    if mode == "mass_vs_lifetime":
        graph.GetYaxis().SetTitleSize(0.035)
        graph.GetYaxis().SetTitleOffset(1.2)
        graph.GetYaxis().SetLabelSize(0.03)
        
        graph.GetXaxis().SetTitleSize(0.035)
        graph.GetXaxis().SetTitleOffset(1.3)
        graph.GetXaxis().SetLabelSize(0.03)
    elif mode == "xsec_vs_mass" or "coupling_vs_mass":
        graph.GetYaxis().SetTitleSize(0.07)
        graph.GetYaxis().SetTitleOffset(1.2)
        graph.GetYaxis().SetLabelSize(0.07)
    
        graph.GetXaxis().SetTitleSize(0.07)
        graph.GetXaxis().SetTitleOffset(1.0)
        graph.GetXaxis().SetLabelSize(0.07)
    else:
        graph.GetXaxis().SetLabelSize(0.1)
        graph.GetXaxis().SetTitleSize(0.1)
        graph.GetXaxis().SetTitleOffset(1.0)
        
        graph.GetYaxis().SetLabelSize(0.1)
        graph.GetYaxis().SetTitleSize(0.1)
        graph.GetYaxis().SetTitleOffset(0.7)

    graph.GetXaxis().SetTitleFont(42)
    graph.GetYaxis().SetTitleFont(42)

    canvases[mode].cd()
    
    if mode == "coupling_vs_mass":
        gPad.SetLogy()
        graph.SetMinimum(5e-4)
        graph.SetMaximum(0.2e1)
        graph.GetXaxis().SetLimits(0, max_x)
    elif mode == "mass_vs_lifetime":
        gPad.SetLogx()
        gPad.SetLogy()
        graph.SetMinimum(2e-1)
        graph.SetMaximum(max_x)
        graph.GetXaxis().SetLimits(0.9e-6, 1.1e4)
    elif mode == "xsec_vs_lifetime":
        gPad.SetLogy()
        graph.SetMinimum(0)
        graph.SetMaximum(max_x)
        graph.GetXaxis().SetLimits(1e-4, 20)
    elif mode == "xsec_vs_mass":
        gPad.SetLogy()
        graph.SetMinimum(3e-6)
        # graph.SetMinimum(5e-5)
        graph.SetMaximum(1e-2)
        graph.GetXaxis().SetLimits(0, max_x)
    
  
def interpolate_empty_error_bands(graph):
    for i_point in range(1, graph.GetN()-1):
        x = graph.GetPointX(i_point)
        y = graph.GetPointY(i_point)
        
        y_up = graph.GetErrorYhigh(i_point)
        
        if y+y_up > 49:
            x_previous = graph.GetPointX(i_point - 1)
            y_previous = graph.GetPointY(i_point - 1)
            y_previous_high = y_previous + graph.GetErrorYhigh(i_point-1)

            x_next = graph.GetPointX(i_point + 1)
            y_next = graph.GetPointY(i_point + 1)
            y_next_high = y_next + graph.GetErrorYhigh(i_point + 1)
            
            a = (y_previous_high-y_next_high)/(x_previous-x_next)
            b = y_previous_high - a*x_previous

            y_new = a * x + b
            y_new -= y
            
            graph.SetPointEYhigh(i_point, y_new)


def get_hllhc_graph(input_graph, with_errors=False):
    graph_hllhc = TGraphAsymmErrors(input_graph)
    graph_hllhc.SetFillColorAlpha(hllhc_expected_color, 0.1)
    graph_hllhc.SetLineColor(hllhc_expected_color)
    graph_hllhc.SetMarkerSize(0)
    graph_hllhc.SetLineStyle(2)
    graph_hllhc.SetLineWidth(3)
    
    for i in range(graph_hllhc.GetN()):
        if not with_errors:
            graph_hllhc.SetPointError(i, 0, 0, 0, graph_hllhc.GetPointY(i) - graph_hllhc.GetPointY(i) / 20)
        graph_hllhc.SetPoint(i, graph_hllhc.GetPointX(i), graph_hllhc.GetPointY(i) / 20)
    
    return graph_hllhc
    
    
def get_arrows(mode):
    x_pos = 5
    y_min = 5e-4 if mode == "xsec_vs_mass" else 7e-2
    y_max = 2e-3 if mode == "xsec_vs_mass" else 3e-1
    
    arrow_150 = TArrow(x_pos, y_min, x_pos, y_max, 0.01, "|>")
    arrow_150.SetLineColor(run2_expected_color)
    arrow_150.SetLineWidth(2)
    arrow_150.Draw()
    
    arrow_3000 = TArrow(x_pos, y_min / 20, x_pos, y_max / 20, 0.01, "|>")
    arrow_3000.SetLineColor(hllhc_expected_color)
    arrow_3000.SetLineWidth(2)
    arrow_3000.Draw()
    
    return arrow_150, arrow_3000
    
    
def get_lumi_labels(mode):
    x_pos_150 = 0.6
    x_pos_3000 = 0.62
    y_pos_150 = 0.72 if mode == "xsec_vs_mass" else 0.68
    y_pos_3000 = 0.44 if mode == "xsec_vs_mass" else 0.39
    angle = 17 if mode == "xsec_vs_mass" else 11
    
    lumi_150 = TLatex(x_pos_150, y_pos_150, "150 fb^{-1}")
    lumi_150.SetNDC(True)
    lumi_150.SetTextColor(run2_expected_color)
    lumi_150.SetTextFont(42)
    lumi_150.SetTextAngle(angle)
    lumi_150.Draw()

    lumi_3000 = TLatex(x_pos_3000, y_pos_3000, "3 ab^{-1}")
    lumi_3000.SetNDC(True)
    lumi_3000.SetTextColor(hllhc_expected_color)
    lumi_3000.SetTextFont(42)
    lumi_3000.SetTextAngle(angle)
    lumi_3000.Draw()
    
    return lumi_150, lumi_3000


def save_canvas(theory_line, graph_mean, graph_1sigma, graph_2sigma, mode):
    
    gPad.SetLeftMargin(0.17)
    gPad.SetBottomMargin(0.20)
    
    
    canvases[mode].cd()
    
    # graph_2sigma.Draw("A3")
    
    graph_1sigma.SetFillColor(run2_1sigma_color)
    graph_1sigma.Draw("A3")

    graph_mean.SetLineStyle(2)
    graph_mean.SetLineWidth(3)
    graph_mean.SetLineColor(run2_expected_color)
    graph_mean.Draw("Lsame")
    
    graph_hllhc = get_hllhc_graph(graph_1sigma, with_errors=False)
    # graph_hllhc.Draw("L3same")
    graph_hllhc.Draw("LXsame")
    
    if mask_masses:
        boxes = []
        y_low = 1e-3 if mode == "coupling_vs_mass" else 5e-6
        y_high = 5e-1 if mode == "coupling_vs_mass" else 1e-2

        for low, high in regions_to_mask.values():
            if high > 90:
                high = 87

            boxes.append(TBox(low, y_low, high, y_high))
            boxes[-1].Draw()
            boxes[-1].SetFillColor(kWhite)
            boxes[-1].SetLineColor(kWhite)

    legend = TLegend(0.17, 0.75, 0.45, 0.9)

    lumi_label = get_lumi_label(mode)
    lumi_label.Draw()

    lumi_150, lumi_3000 = get_lumi_labels(mode)
    lumi_150.Draw()
    lumi_3000.Draw()

    arrow_150, arrow_3000 = get_arrows(mode)
    arrow_150.Draw()
    arrow_3000.Draw()
    
    legend.AddEntry(graph_mean, "Median expected", "l")
    legend.AddEntry(graph_1sigma, "68% expected", "f")
    # legend.AddEntry(graph_2sigma, "95% expected [150 fb^{-1}]  ", "f")
    # legend.AddEntry(graph_hllhc, "Median expected [3 ab^{-1}]  ", "l")
    # legend.AddEntry(graph_2sigma, "95% expected", "f")
    legend.Draw()

    if draw_1pb_line:
        line_1pb = TF1("1pb", "1", 0, 100)
        line_1pb.SetLineColor(kBlack)
        line_1pb.SetLineStyle(2)
        line_1pb.Draw("same")
    
    canvases[mode].Update()
    canvases[mode].SaveAs(f"{mode}.pdf")



    

def save_double_canvas(theory_line, graph_mean, graph_1sigma, graph_2sigma,
                       theory_line_coupling, graph_mean_coupling, graph_1sigma_coupling, graph_2sigma_coupling):
    legend = TLegend(0.61, 0, 1, 0.7)
    
    mode = "xsec_and_coupling"
    canvases[mode].Divide(1, 2)
    canvases[mode].cd(1)
    gPad.SetLogy()
    gPad.SetTopMargin(0.3)
    gPad.SetLeftMargin(0.15)
    gPad.SetBottomMargin(0.00)
    gPad.SetRightMargin(0.4)

    graph_2sigma.Draw("A3")

    graph_hllhc = get_hllhc_graph(graph_mean)
    graph_hllhc.Draw("3Lsame")

    graph_shade = TGraphAsymmErrors(graph_mean)
    graph_shade.SetFillColorAlpha(run2_1sigma_color, 0.1)
    graph_shade.SetLineColor(kWhite)
    graph_shade.SetMarkerSize(0)

    for i in range(graph_shade.GetN()):
        graph_shade.SetPointError(i, 0, 0, 0, 1e9)

    graph_shade.Draw("3same")

    graph_2sigma.Draw("3same")
    
    graph_1sigma.SetFillColor(run2_1sigma_color)
    graph_1sigma.Draw("3same")
    graph_mean.SetLineStyle(2)
    graph_mean.SetLineColor(run2_expected_color)
    graph_mean.SetLineWidth(3)
    graph_mean.Draw("Lsame")

    if mask_masses:
        boxes_1 = []
        y_low = 1e-5
        y_high = 4.8e-1
        
        for low, high in regions_to_mask.values():
            if high > 90:
                high = 87
            
            boxes_1.append(TBox(low, y_low, high, y_high))
            boxes_1[-1].Draw()
            boxes_1[-1].SetFillColor(kWhite)
            boxes_1[-1].SetLineColor(kWhite)
    
    if theory_line is not None:
        theory_line.SetLineColor(theory_color)
        theory_line.SetLineWidth(3)
        theory_line.Draw("Lsame")
        legend.AddEntry(theory_line, "c_{tt}/f_{a} = 1/TeV", "l")
    
    lumi_label = get_lumi_label(mode)
    lumi_label.Draw()
    
    legend.AddEntry(graph_mean, "Median expected [150 fb^{-1}]  ", "l")
    legend.AddEntry(graph_1sigma, "68% expected [150 fb^{-1}]  ", "f")
    legend.AddEntry(graph_2sigma, "95% expected [150 fb^{-1}]  ", "f")
    legend.AddEntry(graph_hllhc, "Median expected [3 ab^{-1}]  ", "l")
    
    box_3 = TBox(-2, 1e-5, -0.1, 5e-5)
    box_3.SetFillColor(kWhite)
    box_3.SetLineColor(kWhite)
    # box_3.Draw()

    canvases[mode].cd(2)
    gPad.SetLogy()
    gPad.SetTopMargin(0.00)
    gPad.SetLeftMargin(0.15)
    gPad.SetBottomMargin(0.3)
    gPad.SetRightMargin(0.4)

    graph_2sigma_coupling.Draw("A3")

    graph_hllhc_coupling = cross_section_to_coupling(graph_hllhc)
    graph_hllhc_coupling.SetFillColorAlpha(hllhc_expected_color, 0.1)
    graph_hllhc_coupling.SetLineColor(hllhc_expected_color)
    graph_hllhc_coupling.SetLineStyle(2)
    graph_hllhc_coupling.SetLineWidth(3)
    graph_hllhc_coupling.SetMarkerSize(0)
    graph_hllhc_coupling.Draw("3Lsame")

    graph_shade_coupling = TGraphAsymmErrors(graph_2sigma_coupling)
    graph_shade_coupling.SetFillColorAlpha(run2_1sigma_color, 0.1)
    graph_shade_coupling.SetLineColor(kWhite)
    graph_shade_coupling.SetMarkerSize(0)

    for i in range(graph_shade_coupling.GetN()):
        graph_shade_coupling.SetPointError(i, 0, 0, 0, 1e9)

    graph_shade_coupling.Draw("3same")

    graph_2sigma_coupling.Draw("3same")
    
    graph_1sigma_coupling.SetFillColor(run2_1sigma_color)
    graph_1sigma_coupling.Draw("3same")
    graph_mean_coupling.SetLineStyle(2)
    graph_mean_coupling.Draw("Lsame")
    
    if mask_masses:
        boxes_2 = []
        y_low = 1e-2
        y_high = 1.9
    
        for low, high in regions_to_mask.values():
            if high > 90:
                high = 87
        
            boxes_2.append(TBox(low, y_low, high, y_high))
            boxes_2[-1].Draw()
            boxes_2[-1].SetFillColor(kWhite)
            boxes_2[-1].SetLineColor(kWhite)

    theory_line_coupling.SetLineColor(theory_color)
    # theory_line_coupling.Draw("Lsame")

    canvases[mode].cd(1)
    legend.Draw()
    
    canvases[mode].Update()
    canvases[mode].SaveAs(f"{mode}.pdf")


def main():
    file = TFile.Open(input_path)
    
    graph_mean = file.Get("limits_mean")
    graph_1sigma = file.Get("limits_1_sigma")
    graph_2sigma = file.Get("limits_2_sigma")

    graph_1sigma.Print()
    
    if ctau_limits:
    
        graph_mean = convert_mm_to_m(graph_mean)
        graph_1sigma = convert_mm_to_m(graph_1sigma)
        graph_2sigma = convert_mm_to_m(graph_2sigma)

        interpolate_empty_error_bands(graph_2sigma)

        theory_line = TGraph()
        i_point = 0

        for mass in logspace(-1, 1, 100):
            ctau = find_lifetime_for_mass(mass, coupling, Lambda)
            theory_line.SetPoint(i_point, ctau, mass)
            i_point += 1
        
        mode = "mass_vs_lifetime"
        prepare_2sigma_graph(graph_2sigma, "c#tau_{0} (m)", "m_{a} (GeV)", mode)
        save_canvas(theory_line, graph_mean, graph_1sigma, graph_2sigma, mode)

    else:
        theory_line = TGraph()
        i_point = 0
    
        for mass, x_sec in alp_cross_section_only_top_coupling.items():
            theory_line.SetPoint(i_point, mass, x_sec)
            i_point += 1
            
        mode = "xsec_vs_mass"
        prepare_2sigma_graph(graph_1sigma, "m_{a} [GeV]", "#sigma(pp#rightarrow t#bar{t}a) [pb] ", mode)
        save_canvas(theory_line, graph_mean, graph_1sigma, graph_2sigma, mode)
    
        theory_line_lifetime = mass_to_lifetime(theory_line, coupling, Lambda)
        graph_mean_lifetime = mass_to_lifetime(graph_mean, coupling, Lambda)
        graph_1sigma_lifetime = mass_to_lifetime(graph_1sigma, coupling, Lambda)
        graph_2sigma_lifetime = mass_to_lifetime(graph_2sigma, coupling, Lambda)
    
        theory_line_coupling = cross_section_to_coupling(theory_line)
        graph_mean_coupling = cross_section_to_coupling(graph_mean)
        graph_1sigma_coupling = cross_section_to_coupling(graph_1sigma)
        graph_2sigma_coupling = cross_section_to_coupling(graph_2sigma)

        mode = "xsec_vs_lifetime"
        prepare_2sigma_graph(graph_2sigma_lifetime, "<#beta#gamma>c#tau [cm]", "#sigma(pp#rightarrow t#bar{t}a) [pb]", mode)
        save_canvas(theory_line_lifetime, graph_mean_lifetime, graph_1sigma_lifetime, graph_2sigma_lifetime, mode)

        mode = "coupling_vs_mass"
        prepare_2sigma_graph(graph_1sigma_coupling, "m_{a} [GeV]", "c_{tt}/f_{a} [TeV^{-1} ]    ", mode)
        save_canvas(theory_line_coupling, graph_mean_coupling, graph_1sigma_coupling, graph_2sigma_coupling, mode)
        
        save_double_canvas(theory_line, graph_mean, graph_1sigma, graph_2sigma,
                           theory_line_coupling, graph_mean_coupling, graph_1sigma_coupling, graph_2sigma_coupling)
    


if __name__ == "__main__":
    main()
