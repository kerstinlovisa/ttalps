from math import log10

from ROOT import TFile, TGraph, TGraphAsymmErrors, TCanvas, TF1, gPad

base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/"

limits_variants = [
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e4mm",
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e5mm",
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e6mm",
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-2e6mm",
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-3e6mm_moreStats",
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-5e6mm",
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-8e6mm",
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-1e7mm",
    "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_ctau-2e7mm",
]


def crosses_one_pb(graph, take_error=None):
    
    has_point_above_one = False
    has_point_below_one = False
    
    for i_point in range(graph.GetN()):
        y = graph.GetPointY(i_point)
        
        if take_error == "up":
            y += graph.GetErrorYhigh(i_point)
        elif take_error == "down":
            y -= graph.GetErrorYlow(i_point)
        
        if y < 1:
            has_point_below_one = True
            
        if y > 1:
            has_point_above_one = True
        
    return has_point_above_one and has_point_below_one


def get_ctau_value(name):
    
    ctau = name.split("ctau-")[-1]
    ctau = ctau.split("mm")[0]
    ctau = ctau.replace("m", "-")
    ctau = float(ctau)
    
    return ctau


def get_mass_closest_to_1pb(graph, take_error=None):
    if not crosses_one_pb(graph, take_error=take_error):
        print("\tline doesn't cross 1 pb.")
        
        if take_error == "down":
            return 0.3
        elif take_error == "up":
            return 50
        
        return 0
    
    point_before = None
    point_after = None
    
    for i_point in range(graph.GetN()-1):
    
        x_1 = graph.GetPointX(i_point)
        y_1 = graph.GetPointY(i_point)
        e_1_up = graph.GetErrorYhigh(i_point)
        e_1_down = graph.GetErrorYlow(i_point)

        x_2 = graph.GetPointX(i_point+1)
        y_2 = graph.GetPointY(i_point+1)
        e_2_up = graph.GetErrorYhigh(i_point+1)
        e_2_down = graph.GetErrorYlow(i_point + 1)
    
        if take_error == "up":
            y_1 += e_1_up
            y_2 += e_2_up
        elif take_error == "down":
            y_1 -= e_1_down
            y_2 -= e_2_down
    
        if y_1 < 0 or y_2 < 0:
            print("below zero... skipping")
            continue
    
        if (y_1 > 1 > y_2) or (y_1 < 1 < y_2):
            point_before = (x_1, y_1)
            point_after = (x_2, y_2)
            break

    a = (log10(point_before[1])-log10(point_after[1]))/(point_before[0]-point_after[0])
    b = log10(point_before[1])-a*point_before[0]
    mass = -b/a
    return mass


def get_error_graph(graph, side):
    
    output_graph = TGraph()
    
    for i_point in range(graph.GetN()):
        x = graph.GetPointX(i_point)
        y = graph.GetPointY(i_point)
        
        if side == "up":
            y += graph.GetErrorYhigh(i_point)
        elif side == "down":
            y -= graph.GetErrorYlow(i_point)
        else:
            print(f"Unrecognized side option: {side}")
            return None
        
        output_graph.SetPoint(i_point, x, y)
        
    return output_graph
    

def get_mass_closest_to_1pb_from_fit(graph, name, take_error=None, params=None):
    if not crosses_one_pb(graph, take_error=take_error):
        print("\tline doesn't cross 1 pb.")
        
        if take_error == "down":
            return 0.3, None
        elif take_error == "up":
            return 50, None
        
        return 0, None
    
    canvas = TCanvas("canvas", "canvas", 800, 600)
    canvas.cd()
    
    gPad.SetLogy()
    
    if take_error:
        graph = get_error_graph(graph, take_error)
    
    fun = TF1("fun", "[0]/([1]*x)+[2]", 0, 10)
    
    scale = 1.2
    
    if params is None:
        fun.SetParameter(0, 1)  # 0.7, 0.2
        fun.SetParameter(1, 0.15)  # 0.08, 0.18
        fun.SetParameter(2, -0.4)  # -0.08, -0.005
    else:
        fun.SetParameter(0, params[0])
        fun.SetParameter(1, params[1])
        fun.SetParameter(2, params[2])
        
        if params[2] > 0:
            fun.SetParLimits(2, params[2]/scale, params[2]*scale)
        else:
            fun.SetParLimits(2, params[2]*scale, params[2]/scale)
    
    graph.Fit(fun, "", "", 0, 10)
    
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.0)
    graph.Draw("APE")
    
    canvas.Update()
    canvas.SaveAs(f"conversion_fit_{name}.pdf")
    
    mass = fun.GetX(1.0)
    
    return mass, (fun.GetParameter(0), fun.GetParameter(1), fun.GetParameter(2))


def main():
    
    output_graph_mean = TGraph()
    output_graph_1sigma = TGraphAsymmErrors()
    output_graph_2sigma = TGraphAsymmErrors()
    
    files = {}
    
    i_point=0
    
    for limits_name in limits_variants:
        files[limits_name] = TFile.Open(f"{base_path}limits_{limits_name}.root")
        graph_mean = files[limits_name].Get("limits_mean")
        graph_1sigma = files[limits_name].Get("limits_1_sigma")
        graph_2sigma = files[limits_name].Get("limits_2_sigma")
        
        print(f"\n\nLoading limits: {limits_name}")

        ctau = get_ctau_value(limits_name)
        
        if not crosses_one_pb(graph_mean):
            print("Main limit doesn't cross 1 pb line. Skipping...")
            continue
            
        print(f"This limit crosses 1 pb line and will be used. (ctau={ctau})")

        print("\tmean")
        mass = get_mass_closest_to_1pb(graph_mean)
        # mass, params = get_mass_closest_to_1pb_from_fit(graph_1sigma, ctau)
        
        print("\tsigma1 up")
        mass_1sigma_up = get_mass_closest_to_1pb(graph_1sigma, take_error="up")
        # mass_1sigma_up, _ = get_mass_closest_to_1pb_from_fit(graph_1sigma, f"{ctau}_1up", take_error="up", params=params)
        print("\tsigma1 down")
        mass_1sigma_down = get_mass_closest_to_1pb(graph_1sigma, take_error="down")
        # mass_1sigma_down, _ = get_mass_closest_to_1pb_from_fit(graph_1sigma, f"{ctau}_1down", take_error="down", params=params)
        print("\tsigma2 up")
        mass_2sigma_up = get_mass_closest_to_1pb(graph_2sigma, take_error="up")
        # mass_2sigma_up, _ = get_mass_closest_to_1pb_from_fit(graph_2sigma, f"{ctau}_2up", take_error="up", params=params)
        print("\tsigma2 down")
        mass_2sigma_down = get_mass_closest_to_1pb(graph_2sigma, take_error="down")
        # mass_2sigma_down, _ = get_mass_closest_to_1pb_from_fit(graph_2sigma, f"{ctau}_2down", take_error="down", params=params)
        
        print(f"{mass_1sigma_up=}, {mass_1sigma_down=}, {mass_2sigma_up=}, {mass_2sigma_down=}")
        print(f"{ctau=}, {mass=}")
        output_graph_mean.SetPoint(i_point, ctau, mass)

        output_graph_1sigma.SetPoint(i_point, ctau, mass)
        output_graph_1sigma.SetPointError(i_point, 0, 0, mass-mass_1sigma_down, mass_1sigma_up-mass)

        output_graph_2sigma.SetPoint(i_point, ctau, mass)
        output_graph_2sigma.SetPointError(i_point, 0, 0, mass-mass_2sigma_down, mass_2sigma_up-mass)

        i_point += 1
        
    output_file = TFile("limits_ctau_vs_mass.root", "recreate")
    output_file.cd()

    output_graph_mean.SetMarkerStyle(20)
    output_graph_mean.SetMarkerSize(1.0)
    output_graph_mean.SetName("limits_mean")

    output_graph_1sigma.SetMarkerStyle(20)
    output_graph_1sigma.SetMarkerSize(1.0)
    output_graph_1sigma.SetName("limits_1_sigma")

    output_graph_2sigma.SetMarkerStyle(20)
    output_graph_2sigma.SetMarkerSize(1.0)
    output_graph_2sigma.SetName("limits_2_sigma")

    output_graph_mean.Write()
    output_graph_1sigma.Write()
    output_graph_2sigma.Write()
    output_file.Close()


if __name__ == "__main__":
    main()