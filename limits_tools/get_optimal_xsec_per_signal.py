import subprocess
from sys import exit
from optparse import OptionParser
import os

from ROOT import TFile
import limits_params as params

# sample = "1e4mm_updated"
sample = "1e5mm_updated"
# sample = "1e6mm_updated"
# sample = "2e6mm_updated"
# sample = "3e6mm_updated"
# sample = "5e6mm_updated"
# sample = "8e6mm_updated"
# sample = "1e7mm_updated"
# sample = "2e7mm_updated"
# sample = "2e8mm_updated"
# sample = "default"
# sample = "default_non-muon-mothers"


sample_short = sample.split("mm")[0]
sample_short = sample_short.split("_")[0]

desired_n_events = 10


def get_xsec_for_signal(signal):
    
    (input_file_name, n_generated_events, cross_section) = signal
    
    file = TFile.Open(input_file_name)
    hist = file.Get(params.hist_name)

    if not file or not hist:
        print(f"couldn't open hist: {params.hist_name} from file: {input_file_name}")

    n_signal_events = 0
    
    for i_bin in range(hist.GetNbinsX()):
        bin_content = float(hist.GetBinContent(i_bin + 1))
        n_signal_events += bin_content / n_generated_events * params.lumi
    
    
    optimal_xsec = desired_n_events/n_signal_events
    
    print(f"Optimal cross section: {optimal_xsec} pb")
    

def main():
    for _, (mass, signal) in params.signals[sample_short].items():
        
        print(f"{mass=}")
        
        signal = list(signal)
        signal[0] = params.get_base_path(sample) + signal[0]
        
        get_xsec_for_signal(signal)
        

    
if __name__ == "__main__":
    main()
