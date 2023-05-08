from math import sqrt, pi
from numpy import logspace

from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, TLegend, TGraphAsymmErrors, TBox, kWhite, TF1, kBlack, TLatex, gStyle, gROOT

import physics as ph
from limits_tools import alp_cross_section_only_top_coupling, mass_to_lifetime, cross_section_to_coupling, regions_to_mask, find_lifetime_for_mass

# input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-2e7mm.root"
# input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-default.root"
input_path = "limits_ctau_vs_mass.root"

mask_masses = True
ctau_limits = True
draw_1pb_line = False

Lambda = 4*pi*1000
coupling = 0.5

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
        text.SetTextSize(0.03)
    else:
        text = TLatex(0.6, 0.82, "L = 150 fb^{-1}, #sqrt{s} = 13 TeV")
        text.SetNDC(True)
        text.SetTextSize(0.06)
    gStyle.SetStatStyle(0)
    gStyle.SetTitleStyle(0)
    gROOT.ForceStyle()
    return text


def prepare_2sigma_graph(graph, x_title, y_title, mode):
    graph.SetFillColor(kYellow)
    graph.GetYaxis().SetTitle(y_title)
    graph.GetXaxis().SetTitle(x_title)
    
    if mode == "mass_vs_lifetime":
        graph.GetYaxis().SetTitleSize(0.035)
        graph.GetYaxis().SetTitleOffset(1.2)
        graph.GetYaxis().SetLabelSize(0.03)
        
        graph.GetXaxis().SetTitleSize(0.035)
        graph.GetXaxis().SetTitleOffset(1.3)
        graph.GetXaxis().SetLabelSize(0.03)
    else:
        graph.GetYaxis().SetTitleSize(0.07)
        graph.GetYaxis().SetTitleOffset(0.7)
        graph.GetYaxis().SetLabelSize(0.06)
    
        graph.GetXaxis().SetTitleSize(0.07)
        graph.GetXaxis().SetTitleOffset(1.2)
        graph.GetXaxis().SetLabelSize(0.06)

    canvases[mode].cd()
    
    if mode == "coupling_vs_mass":
        gPad.SetLogy()
        graph.SetMinimum(1e-3)
        graph.SetMaximum(1e3)
        graph.GetXaxis().SetLimits(0, 10)
    elif mode == "mass_vs_lifetime":
        gPad.SetLogx()
        gPad.SetLogy()
        graph.SetMinimum(2e-1)
        graph.SetMaximum(10)
        graph.GetXaxis().SetLimits(0.9e-6, 1.1e4)
    elif mode == "xsec_vs_lifetime":
        gPad.SetLogy()
        graph.SetMinimum(0)
        graph.SetMaximum(10)
        graph.GetXaxis().SetLimits(1e-4, 20)
    elif mode == "xsec_vs_mass":
        gPad.SetLogy()
        graph.SetMinimum(1e-5)
        graph.SetMaximum(1e3)
        graph.GetXaxis().SetLimits(0, 50)
    
  
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

    
def save_canvas(theory_line, graph_mean, graph_1sigma, graph_2sigma, mode):
    
    canvases[mode].cd()
    
    graph_2sigma.Draw("A3")
    
    graph_1sigma.SetFillColor(kGreen + 1)
    graph_1sigma.Draw("3same")

    graph_mean.SetLineStyle(2)
    graph_mean.Draw("Lsame")
    
    if mask_masses:
        boxes = []
        y_low = 3e-3 if mode == "coupling_vs_mass" else 3e-5
        y_high = 5e-1 if mode == "coupling_vs_mass" else 1e-2

        for low, high in regions_to_mask.values():
            if high > 90:
                high = 87

            boxes.append(TBox(low, y_low, high, y_high))
            boxes[-1].Draw()
            boxes[-1].SetFillColor(kWhite)
            boxes[-1].SetLineColor(kWhite)

    legend = TLegend(0.1, 0.75, 0.45, 0.9)

    if theory_line is not None:
        theory_line.SetLineColor(kRed)
        theory_line.Draw("Lsame")
        legend.AddEntry(theory_line, "Model prediction", "l")

    lumi_label = get_lumi_label(mode)
    lumi_label.Draw()
    
    legend.AddEntry(graph_mean, "Median expected", "l")
    legend.AddEntry(graph_1sigma, "68% expected", "f")
    legend.AddEntry(graph_2sigma, "95% expected", "f")
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
    legend = TLegend(0.5, 0.35, 0.9, 0.8)
    
    mode = "xsec_and_coupling"
    canvases[mode].Divide(1, 2)
    canvases[mode].cd(1)
    gPad.SetLogy()
    gPad.SetTopMargin(0.2)
    gPad.SetBottomMargin(0.00)

    graph_2sigma.Draw("A3")
    graph_1sigma.SetFillColor(kGreen + 1)
    graph_1sigma.Draw("3same")
    graph_mean.SetLineStyle(2)
    graph_mean.Draw("Lsame")
    
    if mask_masses:
        boxes_1 = []
        y_low = 3e-5
        y_high = 1e-2
        
        for low, high in regions_to_mask.values():
            if high > 90:
                high = 87
            
            boxes_1.append(TBox(low, y_low, high, y_high))
            boxes_1[-1].Draw()
            boxes_1[-1].SetFillColor(kWhite)
            boxes_1[-1].SetLineColor(kWhite)
    
    if theory_line is not None:
        theory_line.SetLineColor(kRed)
        theory_line.Draw("Lsame")
        legend.AddEntry(theory_line, "Model prediction", "l")
    
    lumi_label = get_lumi_label(mode)
    lumi_label.Draw()
    
    legend.AddEntry(graph_mean, "Median expected", "l")
    legend.AddEntry(graph_1sigma, "68% expected", "f")
    legend.AddEntry(graph_2sigma, "95% expected", "f")
    legend.Draw()

    box_3 = TBox(-2, 1e-5, -0.1, 5e-5)
    box_3.SetFillColor(kWhite)
    box_3.SetLineColor(kWhite)
    box_3.Draw()

    canvases[mode].cd(2)
    gPad.SetLogy()
    gPad.SetTopMargin(0.00)
    gPad.SetBottomMargin(0.2)

    graph_2sigma_coupling.Draw("A3")
    graph_1sigma_coupling.SetFillColor(kGreen + 1)
    graph_1sigma_coupling.Draw("3same")
    graph_mean_coupling.SetLineStyle(2)
    graph_mean_coupling.Draw("Lsame")

    if mask_masses:
        boxes_2 = []
        y_low = 3e-3
        y_high = 5e-1
    
        for low, high in regions_to_mask.values():
            if high > 90:
                high = 87
        
            boxes_2.append(TBox(low, y_low, high, y_high))
            boxes_2[-1].Draw()
            boxes_2[-1].SetFillColor(kWhite)
            boxes_2[-1].SetLineColor(kWhite)

    theory_line_coupling.SetLineColor(kRed)
    theory_line_coupling.Draw("Lsame")
    
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
        prepare_2sigma_graph(graph_2sigma, "m_{a} (GeV)", "#sigma(pp#rightarrow t#bar{t}a) (pb)", mode)
        # prepare_2sigma_graph(graph_2sigma, "m_{a} (GeV)", "#sigma(pp#rightarrow t#bar{t}a) #times BR(a#rightarrow #mu#mu) (pb)", mode)
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
        prepare_2sigma_graph(graph_2sigma_lifetime, "<#beta#gamma>c#tau (cm)", "#sigma(pp#rightarrow t#bar{t}a) #times BR(a#rightarrow #mu#mu) (pb)", mode)
        save_canvas(theory_line_lifetime, graph_mean_lifetime, graph_1sigma_lifetime, graph_2sigma_lifetime, mode)

        mode = "coupling_vs_mass"
        prepare_2sigma_graph(graph_2sigma_coupling, "m_{a} (GeV)", "c_{tt}", mode)
        save_canvas(theory_line_coupling, graph_mean_coupling, graph_1sigma_coupling, graph_2sigma_coupling, mode)
        
        save_double_canvas(theory_line, graph_mean, graph_1sigma, graph_2sigma,
                           theory_line_coupling, graph_mean_coupling, graph_1sigma_coupling, graph_2sigma_coupling)
    


if __name__ == "__main__":
    main()
