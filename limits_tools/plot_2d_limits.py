from math import sqrt, pi

from ROOT import TFile, kGreen, kYellow, TCanvas, gPad, TGraph, kRed, TLegend, TGraphAsymmErrors, TBox, kWhite, TGraph2D, gStyle, kBlack

import physics as ph

base_input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/limits_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_ctau-{}.root"


# list of samples. Empty string "" in ctaus to include means to include non-reweighted (baseline) sample.
samples = {
    # baseline ctau   ctaus to include (mm)                   default ctau (mm)
    # "1mm":          (("0p1000000", "0p5000000", "1p0000000"), 1.0),
    "1e2mm_test_func":        (("", "50p0000000", "10p0000000"), 100.0),
    # "1em4mm":       (("", "0p0000100", "0p0000500"), 1e-4),
}


# ctaus = ("","0p1000000", "0p5000000", "1p0000000")
# ctaus = ("0p1000000", "0p5000000", "1p0000000")
# ctaus = ("0p1000000", "0p5000000", "")
# default_ctau = 1.0 # in mm, or None if should use theoretical value based on mass

Lambda = 4*pi*1000
coupling = 0.5


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


def save_canvas(title, x_title, y_title, z_title, theory_line, graph):
    canvas = TCanvas(title, title, 800, 600)
    canvas.cd()

    gStyle.SetPalette(1)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.0)
    
    # graph.Draw("colz")

    # graph.Draw("p")
    graph.Draw("pcolz")
    # graph.Draw("surf")
    # graph.Draw("col2")
    gPad.SetPhi(0)
    gPad.SetTheta(90)
    
    theory_line.SetLineColor(kRed)
    theory_line.Draw("Lsame")
    
    graph.SetMinimum(2e-7)
    graph.SetMaximum(1e2)

    graph.GetXaxis().SetRangeUser(0, 90)
    graph.GetYaxis().SetLimits(1e-6, 1e3)
    graph.GetZaxis().SetRangeUser(1e-4, 1e-1)

    gPad.SetLogy()
    # gPad.SetLogx()
    gPad.SetLogz()
    
    gPad.SetRightMargin(0.15)
    
    graph.SetTitle("")
    
    graph.GetYaxis().SetTitle(y_title)
    graph.GetXaxis().SetTitle(x_title)
    graph.GetZaxis().SetTitle(z_title)
    
    canvas.Update()
    canvas.SaveAs(f"{title}.pdf")


def main():
    

    limits_graph = TGraph2D()
    theory_line = TGraph()

    theory_ready =False

    i_point = 0
    
    
    one_mass_graph = TGraph()
    one_mass = 8
    
    one_mass_points = []
    
    for ctau_name, (ctaus, default_ctau) in samples.items():
    
        input_path = base_input_path.format(ctau_name)
        file = TFile.Open(input_path)
        
        for ctau in ctaus:
        
            ctau_name = "" if ctau=="" else f"_ctau-{ctau}mm"
            graph_mean = file.Get(f"limits_mean{ctau_name}")
        
            for i_mass in range(graph_mean.GetN()):
                mass = graph_mean.GetPointX(i_mass)
    
                if ctau != "":
                    ctau_value = float(ctau.replace("p", "."))
                elif default_ctau is None:
                    ctau_value = find_lifetime_for_mass(mass)
                else:
                    ctau_value = default_ctau
                
                x_sec = graph_mean.GetPointY(i_mass)
                
                print(f"setting point: {i_point}, {mass}, {ctau_value}, {x_sec}")
                limits_graph.SetPoint(i_point, mass, ctau_value, x_sec)
                
                if mass == one_mass:
                    
                    one_mass_points.append((ctau_value, x_sec))
                    
                    
                
                if not theory_ready:
                    theory_line.SetPoint(i_point, mass, find_lifetime_for_mass(mass))
                
                i_point += 1
            
            theory_ready = True
    
    save_canvas("2d_limits", "m_{a} (GeV)", "c#tau (mm)", "#sigma(pp#rightarrow t#bar{t}a) (pb)", theory_line, limits_graph)

    canvas = TCanvas("1d_limit", "1d_limit", 800, 600)
    canvas.cd()
    
    one_mass_points = sorted(one_mass_points)
    
    for i, (ctau, x_sec) in enumerate(one_mass_points):
        one_mass_graph.SetPoint(i, ctau, x_sec)
    
    one_mass_graph.SetMarkerStyle(20)
    one_mass_graph.SetMarkerColor(kBlack)
    one_mass_graph.Draw("APL")

    one_mass_graph.SetMinimum(1e-4)
    one_mass_graph.SetMaximum(1e-1)
    one_mass_graph.GetXaxis().SetLimits(1e-6, 1e3)
    
    one_mass_graph.GetXaxis().SetTitle("c#tau (mm)")
    one_mass_graph.GetYaxis().SetTitle("#sigma(pp#rightarrow t#bar{t}a) (pb)")
    
    gPad.SetLogy()
    gPad.SetLogx()
    
    
    canvas.Update()
    canvas.SaveAs("1d_limit.pdf")
    
    
if __name__ == "__main__":
    main()
