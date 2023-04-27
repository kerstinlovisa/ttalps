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

sample = "1e2mm_updated"
sample_short = sample.split("mm")[0]

parser = OptionParser()
addDatacardParserOptions(parser)
options, args = parser.parse_args()
options.bin = True  # make a binary workspace


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
        data_card.obs[f"bin{i_bin+1}"] = 0.0
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
    

def save_datacard(processes):
    hists = {}
    files = {}
    
    n_bins = 0
    
    for name, (input_file_name, _, _) in processes.items():
        files[name] = TFile.Open(input_file_name)
        hists[name] = files[name].Get(params.hist_name)

        if not files[name] or not hists[name]:
            print(f"couldn't open hist: {params.hist_name} from file: {input_file_name}")

        n_bins = hists[name].GetNbinsX()
    
    expected = []
    
    for i_bin in range(n_bins):
        bin_dict = {}
        for name, (_, n_generated_events, cross_section) in processes.items():
            bin_dict[name] = float(hists[name].GetBinContent(i_bin + 1)) * params.lumi * cross_section / n_generated_events
            
        if bin_dict["tta"] == 0:
            bin_dict["tta"] = 1e-50
        
        expected.append(bin_dict)
        print(f"Adding bin: {expected[-1]})")
    
    data_card = get_datacard_for_signal(expected)
    
    options.out = params.tmp_combine_file_name
    options.fileName = "./"
    options.verbose = 1
    
    model_builder = CountingModelBuilder(data_card, options)
    model_builder.setPhysics(defaultModel)
    model_builder.doModel()
    

def get_limits_for_signal(signal):
    processes = {
        "ttj": (params.base_path_backgrounds+"ttj.root", params.n_generated_ttj, params.cross_section_ttj),
        "ttmumu": (params.base_path_backgrounds+"ttmumu.root", params.n_generated_ttmumu, params.cross_section_ttmumu),
        "tta": signal,
    }
    
    print("\n\nPreparing datacard\n\n")
    save_datacard(processes)
    
    print("\n\nRunning combine\n\n")
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

            limits_per_signal[name] = get_limits_for_signal(updated_signal)
        
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
