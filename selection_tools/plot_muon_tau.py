from ROOT import TFile, TCanvas, TF1, gPad, kGreen
import physics as ph

file = TFile.Open("test.root")

hist = file.Get("final_selection/final_selection_mass-cuts_dlxy_ratio-max0p1_os_muon_proper_ctau")

default_function = TF1("default_function", "[0]*exp(-x/[1])", 0, 100)
default_function.SetParameter(0, 1)
default_function.SetParameter(1, 1)

canvas = TCanvas("canvas", "canvas", 800, 600)
canvas.cd()

gPad.SetLogy()

hist.Fit(default_function)

hist.Sumw2()

hist.Draw()

hist.GetXaxis().SetRangeUser(0, 0.1)


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

expected_function = TF1("expected_function", "[0]*exp(-x/[1])", 0, 100)
expected_function.SetParameter(0, default_function.GetParameter(0))
expected_function.SetParameter(1, lifetime)



expected_function.SetLineColor(kGreen)
expected_function.Draw("same")

canvas.Update()
canvas.SaveAs("test.pdf")