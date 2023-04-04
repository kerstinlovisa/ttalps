from ROOT import TFile, TCanvas, TF1, gPad, kGreen, kRed
import physics as ph

# file = TFile.Open("/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/tta_mAlp-0p315GeV.root")
file = TFile.Open("/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/tta_test.root")

hist = file.Get("alp_selections/alp_selection_pt-min0p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_os_maxlxy-muon_proper_ctau")
# hist = file.Get("alp_selections/alp_selection_pt-min0p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_os_maxlxy-muon_proper_ctau")

fit_max = 0.1


canvas = TCanvas("canvas", "canvas", 800, 600)
canvas.cd()

gPad.SetLogy()



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
print(f"expected lifetime: {lifetime} cm")


lifetime *= 1e1 # cm -> mm

expected_function = TF1("expected_function", "[0]*exp(-x/[1])", 0, fit_max)
expected_function.SetParameter(0, 1)
expected_function.FixParameter(1, lifetime)

hist.Fit(expected_function, "", "", 0, fit_max)

expected_function.SetLineColor(kGreen)
expected_function.Draw("same")

canvas.Update()
canvas.SaveAs("test.pdf")