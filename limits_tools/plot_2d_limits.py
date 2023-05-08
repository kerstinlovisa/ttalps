from math import sqrt, pi

from ROOT import TFile, TCanvas, gPad, TGraph, TLegend, TGraphAsymmErrors, TBox, TGraph2D, gStyle, gApplication, TF1, TF2
from ROOT import TGraph2DErrors
from ROOT import kViolet, kBlue, kCyan, kGreen, kOrange, kRed, kYellow, kWhite, kBlack

import physics as ph

base_input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-{}.root"


samples = {
    "1mm":              1,
    "1e4mm":            1e4,
    "1e5mm":            1e5,
    "1e6mm":            1e6,
    "2e6mm":            2e6,
    "3e6mm_moreStats":  3e6,
    "5e6mm":            5e6,
    "8e6mm":            8e6,
    # "1e7mm":            1e7,
    # "2e7mm":            2e7,
}

Lambda = 4*pi*1000
coupling = 0.5

canvas = TCanvas("2d_limits", "2d_limits", 2880, 1800)
canvas.Divide(3, 2)


def find_lifetime_for_mass(mass):
    
    # ctau = ph.ctaua(mass, coupling, coupling, Lambda) # in cm
    # return ctau * 10 # convert to mm

    lscs = ph.getLSfromctt(coupling, coupling, Lambda, mass)
    gamma_mumu = ph.Gammaatoll(mass, ph.readCmumu(lscs), ph.sm['mmu'], Lambda)
    
    if gamma_mumu == 0:
        return 999999

    lifetime_mumu = ph.sm["c"] * ph.sm["hbar"] / gamma_mumu
    lifetime_mumu *= 10  # convert to mm
    
    return lifetime_mumu


def get_log_bins(min_exp, max_exp, points_per_decade=(1,)):
    bins = []
    
    for exponent in range(min_exp, max_exp):
        for point in points_per_decade:
            bins.append(point * 10 ** exponent)
    
    return bins


def save_canvas(x_title, y_title, z_title, graph):
    canvas.cd(1)

    gStyle.SetPalette(1)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.0)
    
    # graph.Draw("colz")

    graph.Draw("p")
    # graph.Draw("pcolz")
    # graph.Draw("surf")
    # graph.Draw("col2")
    # gPad.SetPhi(0)
    # gPad.SetTheta(90)
    
    # graph.SetMinimum(2e-7)
    # graph.SetMaximum(1e2)

    graph.GetXaxis().SetRangeUser(0, 90)
    graph.GetYaxis().SetLimits(1e-3, 2e8)
    graph.GetZaxis().SetRangeUser(1e-4, 1e-1)

    gPad.SetLogy()
    # gPad.SetLogx()
    gPad.SetLogz()
    
    gPad.SetRightMargin(0.15)
    
    graph.SetTitle("")
    
    graph.GetYaxis().SetTitle(y_title)
    graph.GetXaxis().SetTitle(x_title)
    graph.GetZaxis().SetTitle(z_title)
    



def main():
    gStyle.SetLineScalePS(1)
    limits_graph = TGraph2DErrors()
    
    theory_line = TGraph()
    theory_line.SetLineColor(kRed)
    
    theory_ready = False

    i_point = 0
    
    x_sec_vs_mass_graphs = {}
    x_sec_vs_ctau_graphs = []
    
    for i_ctau, (ctau_name, default_ctau) in enumerate(samples.items()):
    
        input_path = base_input_path.format(ctau_name)
        file = TFile.Open(input_path)
        
        graph_mean = file.Get(f"limits_1_sigma")
    
        x_sec_vs_mass_graphs[default_ctau] = TGraphAsymmErrors()
        x_sec_vs_mass_point = 0
    
        for i_mass in range(graph_mean.GetN()):
            mass = graph_mean.GetPointX(i_mass)
            
            if mass > 10:
                continue
            
            x_sec = graph_mean.GetPointY(i_mass)
            x_sec_err = graph_mean.GetErrorY(i_mass)
            # x_sec_down = graph_mean.GetErrorYlow(i_mass)
            # x_sec_up = graph_mean.GetErrorYhigh(i_mass)
            
            x_sec_vs_mass_graphs[default_ctau].SetPoint(x_sec_vs_mass_point, mass, x_sec)
            x_sec_vs_mass_graphs[default_ctau].SetPointError(x_sec_vs_mass_point, 0, 0, graph_mean.GetErrorYlow(i_mass), graph_mean.GetErrorYhigh(i_mass))
            x_sec_vs_mass_point += 1
            
            if i_ctau == 0:
                x_sec_vs_ctau_graphs.append(TGraphAsymmErrors())

            x_sec_vs_ctau_graphs[i_mass].SetPoint(i_ctau, default_ctau, x_sec)
            x_sec_vs_ctau_graphs[i_mass].SetPointError(i_ctau, 0, 0, graph_mean.GetErrorYlow(i_mass), graph_mean.GetErrorYhigh(i_mass))
            
            print(f"setting point: {i_point}, {mass}, {default_ctau}, {x_sec}")
            limits_graph.SetPoint(i_point, mass, default_ctau, x_sec)
            # limits_graph.SetPointError(i_point, 0, 0, 0, 0, x_sec_down, x_sec_up)
            limits_graph.SetPointError(i_point, 0, 0, x_sec_err)
            
            if not theory_ready:
                theory_line.SetPoint(i_point, mass, find_lifetime_for_mass(mass))
            
            i_point += 1
            
        
            
        theory_ready = True
    
    save_canvas("m_{a} (GeV)", "c#tau (mm)", "#sigma(pp#rightarrow t#bar{t}a) (pb)", limits_graph)
    
    canvas.cd(2)
    gPad.SetLogy()

    colors = (kViolet, kBlue, kCyan + 1, kGreen, kOrange, kRed)
    x_sec_vs_mass_funs = []
    
    a_vs_ctau_graph = TGraphAsymmErrors()
    b_vs_ctau_graph = TGraphAsymmErrors()
    
    for i, (ctau, graph) in enumerate(x_sec_vs_mass_graphs.items()):
        x_sec_vs_mass_funs.append(TF1(f"fun_{i}", "[0]/x+[1]", 0, 10))
        x_sec_vs_mass_funs[-1].SetParameter(0, 1)
        x_sec_vs_mass_funs[-1].SetParameter(1, 0)
        
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1.0)
        graph.SetMarkerColor(colors[i%len(colors)])
        
        graph.Fit(x_sec_vs_mass_funs[-1], "", "", 0.3, 10)
        x_sec_vs_mass_funs[-1].SetLineColor(colors[i%len(colors)])
        
        graph.Draw("APE" if i == 0 else "PEsame")
        x_sec_vs_mass_funs[-1].Draw("same")
        
        a_vs_ctau_graph.SetPoint(i, ctau, x_sec_vs_mass_funs[-1].GetParameter(0))
        a_vs_ctau_graph.SetPointError(i, 0, 0, x_sec_vs_mass_funs[-1].GetParError(0), x_sec_vs_mass_funs[-1].GetParError(0))

        b_vs_ctau_graph.SetPoint(i, ctau, x_sec_vs_mass_funs[-1].GetParameter(1))
        b_vs_ctau_graph.SetPointError(i, 0, 0, x_sec_vs_mass_funs[-1].GetParError(1), x_sec_vs_mass_funs[-1].GetParError(1))
        
        if i == 0:
            graph.GetXaxis().SetTitle("m_a (GeV)")
            graph.GetYaxis().SetTitle("#sigma (pb)")
    
            graph.SetMinimum(1e-5)
            graph.SetMaximum(1e3)
            graph.GetXaxis().SetLimits(0, 10)

    print("\n\n\n")
    canvas.cd(4)
    gPad.SetLogx()
    # gPad.SetLogy()
    
    a_vs_ctau_graph.SetMarkerStyle(20)
    a_vs_ctau_graph.SetMarkerSize(1.0)
    a_vs_ctau_graph.Draw("APE")

    a_vs_ctau_graph.GetXaxis().SetTitle("c#tau (mm)")
    a_vs_ctau_graph.GetYaxis().SetTitle("a")
    
    a_vs_ctau_fun = TF1("a_vs_ctau", "[0]+[1]*x+[2]*pow(x, 2)", 0, 1e8)
    a_vs_ctau_fun.SetParameter(0, 0)
    a_vs_ctau_fun.SetParameter(1, 1)
    a_vs_ctau_fun.SetParameter(2, 0)

    a_vs_ctau_graph.Fit(a_vs_ctau_fun)

    print("\n\n\n")
    canvas.cd(5)
    gPad.SetLogx()
    # gPad.SetLogy()
    b_vs_ctau_graph.SetMarkerStyle(20)
    b_vs_ctau_graph.SetMarkerSize(1.0)
    b_vs_ctau_graph.Draw("APE")

    b_vs_ctau_graph.GetXaxis().SetTitle("c#tau (mm)")
    b_vs_ctau_graph.GetYaxis().SetTitle("b")

    b_vs_ctau_fun = TF1("b_vs_ctau", "[0]+[1]*x+[2]*pow(x, 2)", 0, 1e8)
    b_vs_ctau_fun.SetParameter(0, 0)
    b_vs_ctau_fun.SetParameter(1, 1)
    b_vs_ctau_fun.SetParameter(2, 0)

    b_vs_ctau_graph.Fit(b_vs_ctau_fun)

    print("\n\n\n")

    canvas.cd(6)
    gPad.SetRightMargin(0.2)

    limits_fun = TF2("2d_fun", "([0]+[1]*y+[2]*y*y)/x+([3]+[4]*y+[5]*y*y)", 0, 10, 1e-5, 1e8)
    limits_fun.SetNpy(100000)

    limits_fun_tiny = TF2("2d_fun", "[6]*([0]+[1]*y+[2]*y*y)/x+([3]+[4]*y+[5]*y*y)", 0, 10, 1e-5, 1e8)
    limits_fun_tiny.SetNpy(100000)
    
    limits_fun.FixParameter(0, a_vs_ctau_fun.GetParameter(0))
    limits_fun.FixParameter(1, a_vs_ctau_fun.GetParameter(1))
    limits_fun.FixParameter(2, a_vs_ctau_fun.GetParameter(2))
    limits_fun.FixParameter(3, b_vs_ctau_fun.GetParameter(0))
    limits_fun.FixParameter(4, b_vs_ctau_fun.GetParameter(1))
    limits_fun.FixParameter(5, b_vs_ctau_fun.GetParameter(2))
    limits_graph.Fit(limits_fun)

    limits_fun_tiny.FixParameter(0, a_vs_ctau_fun.GetParameter(0))
    limits_fun_tiny.FixParameter(1, a_vs_ctau_fun.GetParameter(1))
    limits_fun_tiny.FixParameter(2, a_vs_ctau_fun.GetParameter(2))
    limits_fun_tiny.FixParameter(3, b_vs_ctau_fun.GetParameter(0))
    limits_fun_tiny.FixParameter(4, b_vs_ctau_fun.GetParameter(1))
    limits_fun_tiny.FixParameter(5, b_vs_ctau_fun.GetParameter(2))
    limits_fun_tiny.FixParameter(6, 1e9)
    limits_graph.Fit(limits_fun_tiny)
    

    print(f"\n\nFun value at 6 GeV, 1e4 mm: {limits_fun.Eval(6, 1e4)}\n\n")

    gPad.SetLogy()
    gPad.SetLogz()

    # limits_fun.GetXaxis().SetRangeUser(0, 90)
    # limits_fun.GetYaxis().SetLimits(1e4, 2e7)
    # limits_fun.GetZaxis().SetRangeUser(1e-4, 1e-1)
    limits_fun.SetMinimum(1e-6)
    limits_fun.SetMaximum(1e2)

    # limits_fun_tiny.SetMinimum(1e-6)
    # limits_fun_tiny.SetMaximum(1e2)

    limits_fun.Draw("colz")

    limits_fun.GetXaxis().SetTitle("m (GeV)")
    limits_fun.GetYaxis().SetTitle("c#tau (mm)")
    limits_fun.GetZaxis().SetTitle("#sigma (pb)")

    # canvas.cd(1)
    # limits_fun.Draw("surf2same")
    
    canvas.cd(3)
    gPad.SetLogx()
    gPad.SetLogy()

    x_sec_vs_ctau_funs = []

    for i, graph in enumerate(x_sec_vs_ctau_graphs):
        x_sec_vs_ctau_funs.append(TF1(f"fun_{i}", "pow(10, [0]+[1]*log10(x))", 0, 1e8))
        x_sec_vs_ctau_funs[-1].SetParameter(0, 1)
        x_sec_vs_ctau_funs[-1].SetParameter(1, 0)
    
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1.0)
        graph.SetMarkerColor(colors[i % len(colors)])
    
        graph.Fit(x_sec_vs_ctau_funs[-1], "", "", 1e3, 1e8)
        x_sec_vs_ctau_funs[-1].SetLineColor(colors[i % len(colors)])
    
        graph.Draw("APE" if i == 0 else "PEsame")
        x_sec_vs_ctau_funs[-1].Draw("same")

    x_sec_vs_ctau_graphs[0].GetXaxis().SetTitle("c#tau (mm)")
    x_sec_vs_ctau_graphs[0].GetYaxis().SetTitle("#sigma (pb)")

    x_sec_vs_ctau_graphs[0].SetMinimum(1e-4)
    x_sec_vs_ctau_graphs[0].SetMaximum(1e3)
    x_sec_vs_ctau_graphs[0].GetXaxis().SetLimits(1e3, 2e8)
    
    
    canvas.Update()
    
    # gApplication.Run()

    canvas.SaveAs(f"2d_limits.pdf")
    
    output_file = TFile("lifetime_vs_mass_limits_function.root", "recreate")
    output_file.cd()
    limits_fun.SetName("limits")
    limits_fun.Write()

    limits_fun_tiny.SetName("limits_tiny")
    limits_fun_tiny.Write()
    
    output_file.Close()
    
    
    
if __name__ == "__main__":
    main()
