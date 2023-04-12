from ROOT import TH2D, TCanvas, gPad, gStyle

from math import sqrt
from array import array


def get_rlxy(x_1, x_2, y_1, y_2):
    x_2 += 1e-10
    y_2 += 1e-10
    
    return sqrt(((x_1-x_2)**2 + (y_1-y_2)**2)/((x_1+x_2)**2 + (y_1+y_2)**2))


def get_log_bins(min_exp, max_exp, points_per_decade=(1,)):
    bins = []
    
    for exponent in range(min_exp, max_exp):
        for point in points_per_decade:
            bins.append(point * 10 ** exponent)
    
    return bins


def scale_by_bin_width(hist):
    if hist.GetEntries() == 0:
        return hist
    
    for i_bin in range(hist.GetNbinsX()):
        n_entries = hist.GetBinContent(i_bin + 1)
        bin_width = hist.GetXaxis().GetBinWidth(i_bin + 1)
        hist.SetBinContent(i_bin + 1, n_entries / bin_width)
    
    return hist


def main():
    gStyle.SetOptStat(0)

    decade_min = -5
    decade_max = 5

    points_per_decade = [10**(x/10) for x in range(1, 10)]
    points_per_decade.insert(0, 1)
    print(f"{points_per_decade=}")
    epsilon = 0.01

    bins = get_log_bins(decade_min, decade_max, points_per_decade=points_per_decade)
    hist = TH2D("R_{l_{xy}}", "R_{l_{xy}}", len(bins) - 1, array("f", bins), len(bins) - 1, array("f", bins))
    
    for x_1_b in points_per_decade:
        for x_1_e in range(decade_min, decade_max):
            x_1 = (x_1_b+epsilon)*10**x_1_e

            for x_2_b in points_per_decade:
                for x_2_e in range(decade_min, decade_max):
                    x_2 = (x_2_b+epsilon)*10 ** x_2_e
                    # x_2 += 1e-50
                    
                    rlxy = get_rlxy(x_1, x_2, 0, 0)
                    
                    hist.Fill(x_1, x_2, rlxy)
    
    hist = scale_by_bin_width(hist)
    
    canvas = TCanvas("canvas", "canvas", 800, 600)
    canvas.cd()
    
    gPad.SetRightMargin(0.15)
    
    gPad.SetLogx()
    gPad.SetLogy()
    gPad.SetLogz()
    
    hist.Draw("colz")
    hist.GetXaxis().SetTitle("x_{1}")
    hist.GetYaxis().SetTitle("x_{2}")
    
    canvas.Update()
    canvas.SaveAs("r_lxy.pdf")
    
    
if __name__ == "__main__":
    main()
