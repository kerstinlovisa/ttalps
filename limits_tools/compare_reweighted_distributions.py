from ROOT import TFile, TCanvas, kViolet, kBlue, kCyan, kGreen, kOrange, kRed, kBlack, kMagenta, gPad, TLegend, gStyle

base_input_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/"

input_paths = (
    (base_input_path+"tta_test.root", kGreen+2, "original, c#tau = 0.004 mm"),
    # (base_input_path+"tta_test_ctau-0p000001mm.root", kViolet),
    # (base_input_path+"tta_test_ctau-0p000010mm.root", kBlue),
    # (base_input_path+"tta_test_ctau-0p000100mm.root", kCyan+1),
    (base_input_path+"tta_test_ctau-0p001000mm.root", kBlue, "reweighted, c#tau = 0.001 mm"),
    # (base_input_path+"tta_test_ctau-0p010000mm.root", kOrange),
    # (base_input_path+"tta_test_ctau-0p100000mm.root", kRed),
    (base_input_path+"tta_test_ctau-1p000000mm.root", kRed, "reweighted, c#tau = 1 mm"),
)


def main():
    
    canvas = TCanvas("canvas", "canvas", 800, 1200)
    canvas.Divide(1, 2)

    gStyle.SetOptStat(0)

    proper_lifetime_hists = {}
    lxy_rebinned_hists = {}
    
    legend = TLegend(0.3, 0.7, 0.7, 0.9)
    
    for i_file, (input_path, color, title) in enumerate(input_paths):
        print(f"Procesing file: {input_path}")
        
        file = TFile.Open(input_path)

        proper_lifetime_hists[input_path] = file.Get("alp_selections/alp_selection_os_minlxy-muon_proper_ctau_logx")
        lxy_rebinned_hists[input_path] = file.Get("final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_os_maxlxy-muon_lxy_rebinned")

        proper_lifetime_hists[input_path].Rebin(2000)
        proper_lifetime_hists[input_path].Scale(1/proper_lifetime_hists[input_path].GetEntries())
        proper_lifetime_hists[input_path].Sumw2(False)

        lxy_rebinned_hists[input_path].Scale(1 / lxy_rebinned_hists[input_path].GetEntries())
        lxy_rebinned_hists[input_path].Sumw2(False)
        
        proper_lifetime_hists[input_path].SetLineColor(color)
        lxy_rebinned_hists[input_path].SetLineColor(color)
        
        canvas.cd(1)
        gPad.SetLogx()
        proper_lifetime_hists[input_path].SetMaximum(0.1)
        proper_lifetime_hists[input_path].GetXaxis().SetRangeUser(1e-5, 0.1)

        proper_lifetime_hists[input_path].SetTitle("")
        proper_lifetime_hists[input_path].GetXaxis().SetTitle("c#tau_{0} (mm)")
        proper_lifetime_hists[input_path].GetYaxis().SetTitle("#events")
        
        proper_lifetime_hists[input_path].DrawCopy("" if i_file == 0 else "same")
        
        legend.AddEntry(proper_lifetime_hists[input_path].Clone(), title, "l")
        
        canvas.cd(2)
        lxy_rebinned_hists[input_path].SetMaximum(1.0)

        lxy_rebinned_hists[input_path].SetTitle("")
        lxy_rebinned_hists[input_path].GetXaxis().SetTitle("l_{xy} (mm)")
        lxy_rebinned_hists[input_path].GetYaxis().SetTitle("#events")
        
        lxy_rebinned_hists[input_path].DrawCopy("" if i_file == 0 else "same")
        
    canvas.cd(1)
    legend.Draw()

    canvas.cd(2)
    legend.Draw()
    
    canvas.Update()
    canvas.SaveAs("reweighted_distributions_comparison.pdf")


if __name__ == "__main__":
    main()