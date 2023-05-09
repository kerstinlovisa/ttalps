from math import sqrt, pi
from numpy import linspace

from ROOT import TFile, TCanvas, gPad, TLegend, TBox, gStyle, gApplication
from ROOT import TGraph, TGraphAsymmErrors, TGraph2D, TGraph2DErrors, TF1, TF2
from ROOT import kViolet, kBlue, kCyan, kGreen, kOrange, kRed, kYellow, kWhite, kBlack

import physics as ph
from limits_tools import find_lifetime_for_mass_mumuonly_noboost

# ----------------------------------------------------------------------------------------------------------------------
# Options

repo_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/"
base_input_path = repo_path + "hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-{}.root"


samples = {
    "1mm":              1,
    "1e4mm":            1e4,
    "1e5mm":            1e5,
    "1e6mm":            1e6,
    "2e6mm":            2e6,
    "3e6mm_moreStats":  3e6,
    "5e6mm":            5e6,
    "8e6mm":            8e6,
    "1e7mm":            1e7,
    "2e7mm":            2e7,
}

Lambda = 4*pi*1000
coupling = 0.5
mass_min = 0.3
mass_max = 10

colors = (kViolet, kBlue, kCyan + 1, kGreen, kOrange, kRed)

re_fit_2d_limits = False
interactive_mode = False
project_2d_graph = False

#
# ----------------------------------------------------------------------------------------------------------------------

canvas = TCanvas("2d_limits", "2d_limits", 2880, 1800)
canvas.Divide(3, 2)


def draw_2d_graph(graph):
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.0)
    
    if project_2d_graph:
        graph.Draw("p colz")
        gPad.SetPhi(0)
        gPad.SetTheta(90)
    else:
        graph.Draw("pe")
    
    graph.GetXaxis().SetRangeUser(0, 90)
    graph.GetYaxis().SetLimits(1e-3, 2e8)
    graph.GetZaxis().SetRangeUser(1e-4, 1e-1)
    graph.SetTitle("")
    graph.GetXaxis().SetTitle("m_{a} (GeV)")
    graph.GetYaxis().SetTitle("c#tau (mm)")
    graph.GetZaxis().SetTitle("#sigma(pp#rightarrow t#bar{t}a) (pb)")


def get_limits_graph(c_tau_name):
    input_path = base_input_path.format(c_tau_name)
    file = TFile.Open(input_path)
    limits_graph = file.Get(f"limits_1_sigma")
    return limits_graph


def get_cross_section_vs_mass_graphs():
    graphs = {}
    
    for i, (c_tau_name, c_tau) in enumerate(samples.items()):
        limits_graph = get_limits_graph(c_tau_name)
        
        graphs[c_tau] = TGraphAsymmErrors()
        graphs[c_tau].SetMarkerStyle(20)
        graphs[c_tau].SetMarkerSize(1.0)
        graphs[c_tau].SetMarkerColor(colors[i % len(colors)])
        
        for i_mass in range(limits_graph.GetN()):
            mass = limits_graph.GetPointX(i_mass)
            
            if mass > mass_max:
                break
            
            graphs[c_tau].SetPoint(i_mass, mass, limits_graph.GetPointY(i_mass))
            graphs[c_tau].SetPointError(i_mass, 0, 0,
                                        limits_graph.GetErrorYlow(i_mass),
                                        limits_graph.GetErrorYhigh(i_mass))
            
    return graphs
    

def get_2d_limits_graph():
    limits_graph_2d = TGraph2DErrors()
    
    i_point = 0
    for c_tau_name, c_tau in samples.items():
        limits_graph = get_limits_graph(c_tau_name)
        
        for i_mass in range(limits_graph.GetN()):
            mass = limits_graph.GetPointX(i_mass)
            
            if mass > mass_max:
                break
            
            limits_graph_2d.SetPoint(i_point, mass, c_tau, limits_graph.GetPointY(i_mass))
            limits_graph_2d.SetPointError(i_point, 0, 0, limits_graph.GetErrorY(i_mass))
            
            i_point += 1
            
    return limits_graph_2d


def get_cross_section_vs_mass_functions():
    functions = {}
    
    for i, (_, c_tau) in enumerate(samples.items()):
        functions[c_tau] = TF1(f"fun_{c_tau}", "[0]/x+[1]", 0, 10)
        functions[c_tau].SetParameter(0, 1)
        functions[c_tau].SetParameter(1, 0)
        functions[c_tau].SetLineColor(colors[i % len(colors)])

    return functions


def get_parameters_graphs(x_sec_vs_mass_functions):
    a_vs_c_tau_graph = TGraphAsymmErrors()
    b_vs_c_tau_graph = TGraphAsymmErrors()
    
    for i, (c_tau, fun) in enumerate(x_sec_vs_mass_functions.items()):
        a_vs_c_tau_graph.SetPoint(i, c_tau, fun.GetParameter(0))
        a_vs_c_tau_graph.SetPointError(i, 0, 0, fun.GetParError(0), fun.GetParError(0))
        
        b_vs_c_tau_graph.SetPoint(i, c_tau, fun.GetParameter(1))
        b_vs_c_tau_graph.SetPointError(i, 0, 0, fun.GetParError(1), fun.GetParError(1))
        
    return a_vs_c_tau_graph, b_vs_c_tau_graph


def fit_cross_section_vs_mass(graphs, functions):
    for c_tau, graph in graphs.items():
        graph.Fit(functions[c_tau], "", "", mass_min, mass_max)


def draw_cross_section_vs_mass(graphs, functions):
    first = True
    
    for c_tau, graph in graphs.items():
        graph.Draw("APE" if first else "PEsame")
        
        functions[c_tau].Draw("same")
        
        graph.GetXaxis().SetTitle("m_a (GeV)")
        graph.GetYaxis().SetTitle("#sigma (pb)")
        
        graph.SetMinimum(1e-5)
        graph.SetMaximum(1e3)
        graph.GetXaxis().SetLimits(0, 10)
        
        first = False
        

def draw_params_graph(graph, name):
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.0)
    graph.Draw("APE")

    graph.GetXaxis().SetTitle("c#tau (mm)")
    graph.GetYaxis().SetTitle(name)


def get_params_function(name):
    fun = TF1(f"{name}_vs_c_tau", "[0]+[1]*x+[2]*pow(x, 2)", 0, 1e8)
    fun.SetParameter(0, 0)
    fun.SetParameter(1, 1)
    fun.SetParameter(2, 0)
    
    return fun


def get_2d_limits_function(a_vs_c_tau_fun, b_vs_c_tau_fun, tiny=False):
    fun = TF2("2d_fun", "[6]*([0]+[1]*y+[2]*y*y)/x+([3]+[4]*y+[5]*y*y)", 0, 10, 1e-5, 1e8)
    fun.SetNpy(10000)
    
    if re_fit_2d_limits:
        fun.SetParameter(0, a_vs_c_tau_fun.GetParameter(0))
        fun.SetParameter(1, a_vs_c_tau_fun.GetParameter(1))
        fun.SetParameter(2, a_vs_c_tau_fun.GetParameter(2))
        fun.SetParameter(3, b_vs_c_tau_fun.GetParameter(0))
        fun.SetParameter(4, b_vs_c_tau_fun.GetParameter(1))
        fun.SetParameter(5, b_vs_c_tau_fun.GetParameter(2))
    else:
        fun.FixParameter(0, a_vs_c_tau_fun.GetParameter(0))
        fun.FixParameter(1, a_vs_c_tau_fun.GetParameter(1))
        fun.FixParameter(2, a_vs_c_tau_fun.GetParameter(2))
        fun.FixParameter(3, b_vs_c_tau_fun.GetParameter(0))
        fun.FixParameter(4, b_vs_c_tau_fun.GetParameter(1))
        fun.FixParameter(5, b_vs_c_tau_fun.GetParameter(2))
        
    fun.FixParameter(6, 1e9 if tiny else 1)
    
    return fun
    
    
def draw_2d_limits_function(function):
    function.SetMinimum(1e-6)
    function.SetMaximum(1e2)
    function.Draw("colz")
    function.GetXaxis().SetTitle("m (GeV)")
    function.GetYaxis().SetTitle("c#tau (mm)")
    function.GetZaxis().SetTitle("#sigma (pb)")


def print_chi2(function):
    try:
        chi2 = function.GetChisquare()
        ndf = function.GetNDF()
        print(f"chi2/NDF = {chi2}/{ndf} = {chi2/ndf}")
    except ZeroDivisionError:
        print("chi2/NDF unknown, NDF = 0")


def main():
    gStyle.SetPalette(1)
    gStyle.SetLineScalePS(1)
    
    limits_graph = get_2d_limits_graph()
    x_sec_vs_mass_graphs = get_cross_section_vs_mass_graphs()

    # 2d limits (cloud of points)
    canvas.cd(1)
    gPad.SetLogy()
    gPad.SetLogz()
    gPad.SetRightMargin(0.15)
    
    draw_2d_graph(limits_graph)
    
    # xsec vs. mass
    canvas.cd(2)
    gPad.SetLogy()

    x_sec_vs_mass_functions = get_cross_section_vs_mass_functions()
    fit_cross_section_vs_mass(x_sec_vs_mass_graphs, x_sec_vs_mass_functions)
    draw_cross_section_vs_mass(x_sec_vs_mass_graphs, x_sec_vs_mass_functions)

    a_vs_c_tau_graph, b_vs_c_tau_graph = get_parameters_graphs(x_sec_vs_mass_functions)

    # parameter "a"
    canvas.cd(3)
    gPad.SetLogx()
    
    draw_params_graph(a_vs_c_tau_graph, "a")
    a_vs_c_tau_fun = get_params_function("a")
    a_vs_c_tau_graph.Fit(a_vs_c_tau_fun)

    # parameter "b"
    canvas.cd(4)
    gPad.SetLogx()
    
    draw_params_graph(b_vs_c_tau_graph, "b")
    b_vs_c_tau_fun = get_params_function("b")
    b_vs_c_tau_graph.Fit(b_vs_c_tau_fun)

    # 2d fit function
    canvas.cd(5)
    gPad.SetLogy()
    gPad.SetLogz()
    gPad.SetRightMargin(0.2)

    limits_fun = get_2d_limits_function(a_vs_c_tau_fun, b_vs_c_tau_fun, tiny=False)
    limits_fun_tiny = get_2d_limits_function(a_vs_c_tau_fun, b_vs_c_tau_fun, tiny=True)

    limits_graph_tiny = TGraph2DErrors(limits_graph)
    limits_graph_tiny.Scale(1e9)

    if re_fit_2d_limits:
        limits_graph.Fit(limits_fun)
        limits_graph_tiny.Fit(limits_fun_tiny)

    print_chi2(limits_fun)
    print_chi2(limits_fun_tiny)
    draw_2d_limits_function(limits_fun)

    # save results
    canvas.Update()
    canvas.SaveAs(f"2d_limits.pdf")

    output_file = TFile("lifetime_vs_mass_limits_function.root", "recreate")
    output_file.cd()
    limits_fun.SetName("limits")
    limits_fun.Write()

    limits_fun_tiny.SetName("limits_tiny")
    limits_fun_tiny.Write()

    output_file.Close()
    
    if interactive_mode:
        gApplication.Run()


if __name__ == "__main__":
    main()
