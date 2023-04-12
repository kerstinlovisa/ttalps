from ROOT import TFile, TCanvas, TF1, gPad, kGreen, kRed, TH1D
import physics as ph

# file = TFile.Open("/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/tta_mAlp-0p315GeV.root")
file = TFile.Open("/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/tta_test.root")

# hist = file.Get("alp_selections/alp_selection_pt-min0p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_os_maxlxy-muon_proper_ctau")
# hist = file.Get("alp_selections/alp_selection_pt-min0p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_os_maxlxy-muon_proper_ctau")
hist = file.Get("alp_selections/alp_selection_os_minlxy-muon_proper_ctau")


fit_max = 0.1


canvas = TCanvas("canvas", "canvas", 800, 600)
canvas.cd()

# gPad.SetLogy()



hist.Sumw2()
hist.Draw()
hist.GetXaxis().SetRangeUser(0, 0.07)

hist.GetXaxis().SetTitle("c#tau (mm)")
hist.GetYaxis().SetTitle("#events")


default_function = TF1("default_function", "[0]*exp(-x/[1])", 0, fit_max)
default_function.SetParameter(0, 1)
default_function.SetParameter(1, 1)

hist.Fit(default_function, "", "", 0, fit_max)

default_function.SetLineColor(kRed)
default_function.Draw("same")

baseline_lifetime = default_function.GetParameter(1)


print(f"Baseline lifetime:{baseline_lifetime} mm")


def find_lifetime_for_mass(mass):
    Lambda = 1000
    ctau = ph.ctaua(mass, 0.5, 0.5, Lambda)  # in cm

    boost = 1 / mass

    if mass < 3:
        boost *= 223
    elif mass < 20:
        boost *= 230
    elif mass < 30:
        boost *= 240
    elif mass < 50:
        boost *= 260
    else:
        boost *= 296

    # return boost * ctau
    return ctau


lifetime = find_lifetime_for_mass(0.3)
lifetime *= 1e1 # cm -> mm

print(f"expected lifetime: {lifetime} mm")

hists_tmp = {}
weights = {}
hists = {}

# for lifetime in (1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2):
for lifetime in (1e-2,):
    scaled_lifetime_function = TF1("scaled_lifetime_function", "[0]*exp(-x/[1])", 0, fit_max)
    scaled_lifetime_function.SetParameter(0, 1)
    scaled_lifetime_function.FixParameter(1, lifetime)

    hist.Fit(scaled_lifetime_function, "", "", 0, fit_max)

    hists_tmp[lifetime] = TH1D("hist_scaled", "hist_scaled",
                               hist.GetNbinsX(),
                               hist.GetXaxis().GetBinLowEdge(1),
                               hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX())+hist.GetXaxis().GetBinWidth(hist.GetNbinsX()))

    weights[lifetime] = TH1D("weights", "weights",
                             hist.GetNbinsX(),
                             hist.GetXaxis().GetBinLowEdge(1),
                             hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX()) + hist.GetXaxis().GetBinWidth(hist.GetNbinsX()))

    hists[lifetime] = TH1D("hist_scaled", "hist_scaled",
                           hist.GetNbinsX(),
                           hist.GetXaxis().GetBinLowEdge(1),
                           hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX()) + hist.GetXaxis().GetBinWidth(hist.GetNbinsX()))

    for i_bin in range(1, hist.GetNbinsX()+1):
        value = hist.GetXaxis().GetBinCenter(i_bin)
        content = hist.GetBinContent(i_bin)
        
        if content > 0:
            weigth = scaled_lifetime_function.Eval(value)/content
        else:
            weigth = 0
        
        hists_tmp[lifetime].SetBinContent(i_bin, content*weigth)
        weights[lifetime].SetBinContent(i_bin, weigth)
    
    scale = hist.Integral()/hists_tmp[lifetime].Integral()
    weights[lifetime].Scale(scale)

    for i_bin in range(1, hist.GetNbinsX() + 1):
        value = hist.GetXaxis().GetBinCenter(i_bin)
        content = hist.GetBinContent(i_bin)
        weigth = weights[lifetime].GetBinContent(i_bin)
        hists[lifetime].SetBinContent(i_bin, content * weigth)
        
    hists[lifetime].SetLineColor(kGreen+1)
    hists[lifetime].Draw("same")

    scaled_lifetime_function.SetLineColor(kGreen+1)
    scaled_lifetime_function.Draw("same")

canvas.Update()
canvas.SaveAs("test.pdf")