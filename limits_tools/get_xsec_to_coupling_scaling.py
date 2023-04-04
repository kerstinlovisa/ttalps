from ROOT import TGraph, TF1, kGreen, TCanvas, gPad

masses = (0.1, 0.2, 0.3, 0.315, 0.5, 1, 2, 4, 8, 8.5, 10, 20, 40, 50, 70, 80)
# cu3x3	σ (pb)

cross_sections = {
1.0E-03:	(1.180E-07,	1.182E-07,	1.190E-07,	1.174E-07,	1.190E-07,	1.167E-07,	1.181E-07,	1.190E-07,	1.164E-07,	1.155E-07,	1.142E-07,	1.078E-07,	9.147E-08,	8.328E-08,	7.029E-08,	6.439E-08),
1.0E-02:	(1.184E-05,	1.168E-05,	1.187E-05,	1.170E-05,	1.186E-05,	1.173E-05,	1.182E-05,	1.178E-05,	1.166E-05,	1.158E-05,	1.152E-05,	1.087E-05,	9.180E-06,	8.372E-06,	7.062E-06,	6.429E-06),
1.0E-01:	(1.180E-03,	1.184E-03,	1.195E-03,	1.183E-03,	1.173E-03,	1.168E-03,	1.177E-03,	1.151E-03,	1.160E-03,	1.171E-03,	1.152E-03,	1.089E-03,	9.217E-04,	8.371E-04,	7.003E-04,	6.449E-04),
1.0E+00:	(1.175E-01,	1.191E-01,	1.189E-01,	1.169E-01,	1.177E-01,	1.172E-01,	1.184E-01,	1.178E-01,	1.164E-01,	1.155E-01,	1.155E-01,	1.063E-01,	9.202E-02,	8.483E-02,	7.074E-02,	6.487E-02),
1.0E+01:	(1.163E+01,	1.175E+01,	1.188E+01,	1.190E+01,	1.178E+01,	1.163E+01,	1.161E+01,	1.176E+01,	1.158E+01,	1.165E+01,	1.152E+01,	1.091E+01,	9.216E+00,	8.206E+00,	6.987E+00,	6.479E+00),
1.0E+02:	(1.177E+03,	1.192E+03,	1.173E+03,	1.183E+03,	1.186E+03,	1.171E+03,	1.180E+03,	1.178E+03,	1.165E+03,	1.170E+03,	1.143E+03,	1.090E+03,	9.231E+02,	8.479E+02,	7.151E+02,	6.518E+02),
}









# a	0.1200	0.1200	0.1200	0.1200	0.1200	0.1200	0.1200	0.1200	0.1200	0.1200	0.1148	0.1100	0.0919	0.0839	0.0708	0.0646


graphs = {}

for i_mass, mass in enumerate(masses):
    graphs[mass] = TGraph()
    
    for i_point, (c_u3x3, values) in enumerate(cross_sections.items()):
        graphs[mass].SetPoint(i_point, c_u3x3, values[i_mass])
        
        
graphs[0.1].SetMarkerStyle(20)
graphs[0.1].SetMarkerColor(kGreen)



canvas = TCanvas("canvas", "canvas", 800, 600)
canvas.cd()

gPad.SetLogx()
# gPad.SetLogy()


funs = {}
coefficients = {}
coefficients_err = {}

for mass in masses:
    
    funs[mass] = TF1(f"{mass}", "[0]*x*x", 0, 100)
    funs[mass].SetParameter(0, 1)

    graphs[mass].Fit(funs[mass])
    
    coefficients[mass] = funs[mass].GetParameter(0)
    coefficients_err[mass] = funs[mass].GetParError(0)
    
    # if mass == 0.1:
    #     graphs[mass].Draw("AP")
    # else:
    #     graphs[mass].Draw("Psame")


a_vs_mass = TGraphErrors()

for i_point, (mass, coefficient) in enumerate(coefficients.items()):
    print(f"{mass}: {coefficient}")
    a_vs_mass.SetPoint(i_point, mass, coefficient)
    
a_vs_mass.SetMarkerColor(kGreen)
a_vs_mass.SetMarkerStyle(20)

a_vs_mass.Draw("AP")




canvas.Update()
canvas.SaveAs("cross_section_to_coupling.pdf")