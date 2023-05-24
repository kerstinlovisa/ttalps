from ROOT import TGraph, TF1, kGreen, TCanvas, gPad, TGraphErrors

masses = (0.1, 0.2, 0.3, 0.315, 0.35, 0.5, 0.9, 1, 1.25, 2, 2.5, 2.75, 3, 4, 8, 8.25, 8.5, 9, 10, 20, 40, 50, 70, 80)

cross_sections = {
# cu3x3	    σ (pb)
#            0.1,       0.2,        0.3,        0.315,      0.35,       0.5,        0.9,        1,          1.25,           2,          2.5,        2.75,       3           4,          8,          8.5,        9,          10,         20,         40,         50,         70,         80
1.0E-03:	(1.180E-07,	1.182E-07,	1.190E-07,	1.174E-07,	1.172e-07,  1.190E-07,	1.181e-07,  1.167E-07,  1.177e-07,	    1.181E-07,	1.183e-07,  1.172e-07,  1.181e-07,  1.190E-07,  1.155e-07,  1.159e-07,  1.155e-07,  1.164E-07,	1.155E-07,	1.142E-07,	1.078E-07,	9.147E-08,	8.328E-08,	7.029E-08,	6.439E-08),
1.0E-02:	(1.184E-05,	1.168E-05,	1.187E-05,	1.170E-05,	1.202e-05,  1.186E-05,	1.19e-05 ,  1.173E-05,  1.175e-05,  	1.182E-05,	1.165e-05,  1.184e-05,  1.186e-05,  1.178E-05,  1.164e-05,  1.154e-05,  1.155e-05, 	1.166E-05,	1.158E-05,	1.152E-05,	1.087E-05,	9.180E-06,	8.372E-06,	7.062E-06,	6.429E-06),
1.0E-01:	(1.180E-03,	1.184E-03,	1.195E-03,	1.183E-03,	0.001182,   1.173E-03,	0.001186,   1.168E-03,  0.001189,   	1.177E-03,	0.001165,   0.001177,   0.001174,   1.151E-03,  0.001155,   0.001168,   0.001139, 	1.160E-03,	1.171E-03,	1.152E-03,	1.089E-03,	9.217E-04,	8.371E-04,	7.003E-04,	6.449E-04),
1.0E+00:	(1.175E-01,	1.191E-01,	1.189E-01,	1.169E-01,	0.119,      1.177E-01,	0.1189,     1.172E-01,  0.1181,     	1.184E-01,	0.119,      0.1179,     0.1173,     1.178E-01,  0.1164,     0.1151,     0.1151, 	1.164E-01,	1.155E-01,	1.155E-01,	1.063E-01,	9.202E-02,	8.483E-02,	7.074E-02,	6.487E-02),
1.0E+01:	(1.163E+01,	1.175E+01,	1.188E+01,	1.190E+01,	11.69,      1.178E+01,	11.91,      1.163E+01,  11.68,      	1.161E+01,  11.88,      11.66,      11.8,       1.176E+01,  11.68,      11.6,       11.64, 	    1.158E+01,	1.165E+01,	1.152E+01,	1.091E+01,	9.216E+00,	8.206E+00,	6.987E+00,	6.479E+00),
1.0E+02:	(1.177E+03,	1.192E+03,	1.173E+03,	1.183E+03,	1179,       1.186E+03,	1170,       1.171E+03,  1176,       	1.180E+03,	1165,       1169,       1170,       1.178E+03,  1170,       1146,       1164, 	    1.165E+03,	1.170E+03,	1.143E+03,	1.090E+03,	9.231E+02,	8.479E+02,	7.151E+02,	6.518E+02),
}

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

funs = {}
coefficients = {}
coefficients_err = {}

for mass in masses:
    
    funs[mass] = TF1(f"{mass}", "[0]*x*x", 0, 100)
    funs[mass].SetParameter(0, 1)

    graphs[mass].Fit(funs[mass])
    
    coefficients[mass] = funs[mass].GetParameter(0)
    coefficients_err[mass] = funs[mass].GetParError(0)


a_vs_mass = TGraphErrors()

for i_point, (mass, coefficient) in enumerate(coefficients.items()):
    print(f"{mass}: {coefficient:.5f},")
    a_vs_mass.SetPoint(i_point, mass, coefficient)
    a_vs_mass.SetPointError(i_point, 0, coefficients_err[mass])
    

a_of_m_fun = TF1("a_of_m_fun", "[0]*x+[1]", 0, 100)
a_of_m_fun.SetParameter(0, 1)
a_of_m_fun.SetParameter(1, 0)

a_vs_mass.Fit(a_of_m_fun)
    
a_vs_mass.SetMarkerColor(kGreen)
a_vs_mass.SetMarkerStyle(20)
a_vs_mass.Draw("APE")

a_vs_mass.GetXaxis().SetTitle("m_{a} (GeV)")
a_vs_mass.GetYaxis().SetTitle("a")


canvas.Update()
canvas.SaveAs("cross_section_to_coupling.pdf")
