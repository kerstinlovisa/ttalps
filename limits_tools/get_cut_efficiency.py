import subprocess
from sys import exit
from optparse import OptionParser
import os

from HiggsAnalysis.CombinedLimit.DatacardParser import *
from HiggsAnalysis.CombinedLimit.ModelTools import *
from HiggsAnalysis.CombinedLimit.ShapeTools import *
from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from ROOT import TFile, TGraphAsymmErrors

# import ttalps.ttalps.limits_tools.limit_params as params

import limits_params as params

# sample = "1e0mm"
# sample = "1e1mm"
sample = "1e4mm"
# sample = "1e5mm"
# sample = "1e6mm"
# sample = "1e7mm"

# sample = "default"
# sample = "default_non-muon-mothers"
# sample = "default_non-prompt-selection"
# sample = "default_new-dimuon-mass-cuts"

# sample = "2e6mm_updated"
# sample = "3e6mm_updated"
# sample = "5e6mm_updated"
# sample = "8e6mm_updated"
# sample = "2e7mm_updated"
# sample = "2e8mm_updated"



sample_short = sample.split("mm")[0]
sample_short = sample_short.split("_")[0]


def get_efficiency(signal):
    
    input_file_name = signal[0]
    file = TFile.Open(params.get_base_path(sample)+input_file_name)
    hist = file.Get(params.signal_hist_name)

    n_signal_events = 0

    for i_bin in range(hist.GetNbinsX()):
        
        n_signal_events += float(hist.GetBinContent(i_bin + 1))

    n_generated_events = signal[1]
    efficiency = n_signal_events / n_generated_events
    return efficiency


def main():
    lumi_run2 = 150.0 * 1000.0  # pb
    lumi_hllhc = 3000.0 * 1000.0  # pb
    minimum_number_of_events = 10.0
    
    for _, (mass, signal) in params.signals[sample_short].items():
        efficiency = get_efficiency(signal)
        
        
        x_sec_min_run_2 = minimum_number_of_events / (efficiency * lumi_run2)
        x_sec_min_hllhc = minimum_number_of_events / (efficiency * lumi_hllhc)

        print(f"{mass}: {efficiency:.2f}, x_sec_r2: {x_sec_min_run_2:.0e} pb, x_sec_hllhc:{x_sec_min_hllhc:.0e} pb")
        
        
        
        
        
if __name__ == "__main__":
    main()
