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
# sample = "1e4mm"
# sample = "1e5mm"
# sample = "1e6mm"
# sample = "1e7mm"

# sample = "default"
# sample = "default_non-muon-mothers"
# sample = "default_non-prompt-selection"
sample = "default_new-dimuon-mass-cuts"
# sample = "default_ptAlp-ge5GeV"

# sample = "2e6mm_updated"
# sample = "3e6mm_updated"
# sample = "5e6mm_updated"
# sample = "8e6mm_updated"
# sample = "2e7mm_updated"
# sample = "2e8mm_updated"

zero_signal_value = 1e-50
zero_background_value = 0

sample_short = sample.split("mm")[0]
sample_short = sample_short.split("_")[0]

parser = OptionParser()
addDatacardParserOptions(parser)
options, args = parser.parse_args()
options.bin = True  # make a binary workspace

correct_for_branching_ratios = True

branching_ratio_to_muons = {
    0.3: 0.9999516480656298,
    0.35: 0.999954381388671,
    0.5: 0.9998929187578673,
    0.9: 0.9994465135087311,
    1.25: 0.24705198671664572,
    2: 0.17681064813740055,
    2.5: 0.0847743832312974,
    2.75: 0.004604980707690422,
    3.0: 0.003401542021041526,
    4: 0.0018272180991503392,
    8: 0.0010447039648636659,
    8.25: 0.0008904841549107469,
    8.5: 3.9530535748123676e-05,
    9.0: 1.987044074364474e-05,
    10: 1.35213783949236e-05,
}


def init_datacard():
    data_card = Datacard()
    data_card.isSignal = {}
    data_card.keyline = []
    data_card.shapeMap = {}
    data_card.hasShapes = False
    data_card.flatParamNuisances = {}
    data_card.rateParams = {}
    data_card.extArgs = {}
    data_card.rateParamsOrder = set([])
    data_card.frozenNuisances = set([])
    data_card.systematicsShapeMap = {}
    data_card.nuisanceEditLines = []
    data_card.groups = {}
    data_card.discretes = []
    
    return data_card
    

def get_datacard_for_signal(expected):
    data_card = init_datacard()
    
    for i_bin in range(len(expected)):
        data_card.bins.append(f"bin{i_bin+1}")  
        data_card.obs[f"bin{i_bin+1}"] = expected[i_bin]["ttj"] + expected[i_bin]["ttmumu"]
        data_card.exp[f"bin{i_bin+1}"] = expected[i_bin]
    
    data_card.processes = ['tta', 'ttj', 'ttmumu']
    data_card.signals = ['tta']
    
    for process in data_card.processes:
        
        isSignal = process in data_card.signals
        
        data_card.isSignal[process] = isSignal

        for i_bin in range(len(expected)):
            data_card.keyline.append((f"bin{i_bin+1}", process, isSignal))
        
    data_card.systs = [
        ('lumi', False, 'lnN', [],
         {f'bin{i_bin+1}': {'ttj': params.lumi_syst, 'ttmumu': params.lumi_syst, 'tta': params.lumi_syst} for i_bin in range(len(expected))}
         )]
    
    return data_card
    

def save_datacard(processes, mass):
    hists = {}
    files = {}
    
    n_bins = 0
    
    
    
    for name, (input_file_name, _, _) in processes.items():
        files[name] = TFile.Open(input_file_name)
        
        hist_name = params.signal_hist_name if name == "tta" else params.background_hist_name
        print(f"Loading histogram: {hist_name} from file: {input_file_name}")
        
        hists[name] = files[name].Get(hist_name)

        if not files[name] or not hists[name]:
            print(f"couldn't open hist: {hist_name} from file: {input_file_name}")

        n_bins = hists[name].GetNbinsX()
    
    expected = []
    
    n_signal_events = 0
    n_signal_bin_content = 0
    
    for i_bin in range(n_bins):
        bin_dict = {}
        for name, (_, n_generated_events, cross_section) in processes.items():
            bin_content = float(hists[name].GetBinContent(i_bin + 1))
            # bin_width = hists[name].GetXaxis().GetBinWidth(i_bin + 1)
            # bin_content /= bin_width
            
            if name == "tta" and correct_for_branching_ratios:
                bin_content *= branching_ratio_to_muons[mass]
            
            bin_dict[name] = bin_content / n_generated_events * params.lumi * cross_section
            
        if bin_dict["tta"] == 0:
            bin_dict["tta"] = zero_signal_value

        if bin_dict["ttj"] == 0:
            bin_dict["ttj"] = zero_background_value
            
        if bin_dict["ttmumu"] == 0:
            bin_dict["ttmumu"] = zero_background_value

        n_signal_events += bin_dict["tta"]
        n_signal_bin_content += hists["tta"].GetBinContent(i_bin + 1)
        
        expected.append(bin_dict)
        print(f"Adding bin: {expected[-1]})")
    
    print(f"Total number of signal events: {n_signal_events}")
    print(f"Raw total number of signal events: {n_signal_bin_content}")
    
    print(f"{bin_dict=}")
    
    data_card = get_datacard_for_signal(expected)
    
    options.out = params.tmp_combine_file_name
    options.fileName = "./"
    options.verbose = 1
    
    model_builder = CountingModelBuilder(data_card, options)
    model_builder.setPhysics(defaultModel)
    model_builder.doModel()
    

def get_limits_for_signal(signal, mass):
    processes = {
        "ttj": (params.get_base_background_path(sample)+"ttj.root", params.n_generated_ttj, params.cross_section_ttj),
        "ttmumu": (params.get_base_background_path(sample)+"ttmumu.root", params.n_generated_ttmumu, params.cross_section_ttmumu),
        "tta": signal,
    }
    
    print("\n\nPreparing datacard\n\n")
    save_datacard(processes, mass)
    
    print("\n\nRunning combine\n\n")
    print(f"combine {params.tmp_combine_file_name} -M AsymptoticLimits > {params.tmp_output_file_name}")
    os.system(f"combine {params.tmp_combine_file_name} -M AsymptoticLimits > {params.tmp_output_file_name}")
    
    print("\n\nReading limits from combine output\n\n")
    limits = {}
    with open(params.tmp_output_file_name, "r") as file:
        lines = file.readlines()

        for line in lines:
            if "Expected" in line:
                parts = line.split(" ")
                limits[parts[1]] = float(parts[-1])
    
    return limits


def main():
    print("\n\nSaving limits\n\n")
    output_file = TFile(params.output_file_name, "recreate")
    output_file.cd()

    for ctau in params.get_ctaus(sample):

        limits_per_signal = {}

        ctau_name = "" if ctau=="" else f"_ctau-{ctau}mm"

        graph_mean = TGraphAsymmErrors()
        graph_1sigma = TGraphAsymmErrors()
        graph_2sigma = TGraphAsymmErrors()

        graph_mean.SetName(f"limits_mean{ctau_name}")
        graph_1sigma.SetName(f"limits_1_sigma{ctau_name}")
        graph_2sigma.SetName(f"limits_2_sigma{ctau_name}")
    
        i_point = 0

        for name, (mass, signal) in params.signals[sample_short].items():

            updated_signal = list(signal)
 
            if ctau != "":
                updated_signal[0] = updated_signal[0].replace(".root", f"{ctau_name}.root")

            updated_signal[0] = params.get_base_path(sample) + updated_signal[0]

            print(f"{updated_signal=}")

            limits_per_signal[name] = get_limits_for_signal(updated_signal, mass)
        
            reference_x_sec = signal[-1]
        
            value = limits_per_signal[name]["50.0%:"]
            up_1_sigma = abs(limits_per_signal[name]["84.0%:"] - value)
            up_2_sigma = abs(limits_per_signal[name]["97.5%:"] - value)
            down_1_sigma = abs(limits_per_signal[name]["16.0%:"] - value)
            down_2_sigma = abs(limits_per_signal[name][""] - value)

            value *= reference_x_sec
            up_1_sigma *= reference_x_sec
            up_2_sigma *= reference_x_sec
            down_1_sigma *= reference_x_sec
            down_2_sigma *= reference_x_sec
        
            graph_mean.SetPoint(i_point, mass, value)
            graph_1sigma.SetPoint(i_point, mass, value)
            graph_1sigma.SetPointError(i_point, 0, 0, down_1_sigma, up_1_sigma)
            graph_2sigma.SetPoint(i_point, mass, value)
            graph_2sigma.SetPointError(i_point, 0, 0, down_2_sigma, up_2_sigma)
        
            i_point += 1
        
            print(f"Central limit for {name}: {value}")

        output_file.cd()
        graph_mean.Write()
        graph_1sigma.Write()
        graph_2sigma.Write()

    output_file.Close()

    
if __name__ == "__main__":
    main()
