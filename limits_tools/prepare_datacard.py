import subprocess
from sys import exit
from optparse import OptionParser
import os

from HiggsAnalysis.CombinedLimit.DatacardParser import *
from HiggsAnalysis.CombinedLimit.ModelTools import *
from HiggsAnalysis.CombinedLimit.ShapeTools import *
from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from ROOT import TFile, TGraphAsymmErrors

parser = OptionParser()
addDatacardParserOptions(parser)
options,args = parser.parse_args()
options.bin = True # make a binary workspace

lumi = 138.0 # fb-1
lumi_syst = 1.1

n_generated_ttj = 12540000.0
n_generated_ttmumu = 9940000.0

# x_sec in fb
cross_section_ttj = 1.0
cross_section_ttmumu = 1.0

signals = {
#                           mass    file                    n_gen       ref. x_sec (fb)
        "tta_mAlp-0p3GeV":  (0.3, ("tta_mAlp-0p3GeV.root", 1950000.0, 1.0)),
        "tta_mAlp-0p5GeV":  (0.5, ("tta_mAlp-0p5GeV.root", 1659356.0, 1.0)),
        "tta_mAlp-1GeV":    (1.0, ("tta_mAlp-1GeV.root", 1158318.0, 1.0)),
        "tta_mAlp-10GeV":   (10, ("tta_mAlp-10GeV.root", 1127443.0, 1.0)),
    }

base_path = "/nfs/dust/cms/user/lrygaard/ttalps/hists/muon_siblings/"
hist_name = "final_selection/final_selection_mass-max20GeV_muon_lxy_rebinned"

tmp_combine_file_name = "tmp_combine_workspace.root"
tmp_output_file_name = "tmp_output.txt"

output_file_name = "limits.root"

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
         {f'bin{i_bin+1}': {'ttj': lumi_syst, 'ttmumu': lumi_syst, 'tta': lumi_syst} for i_bin in range(len(expected))}
         )]
    
    return data_card
    
def save_datacard(processes):
    hists = {}
    files = {}
    
    n_bins = 0
    
    for name, (input_file_name, _, _) in processes.items():
        files[name] = TFile.Open(base_path + input_file_name)
        hists[name] = files[name].Get(hist_name)
        n_bins = hists[name].GetNbinsX()
    
    expected = []
    
    for i_bin in range(n_bins):
        bin_dict = {}
        for name, (_, n_generated_events, cross_section) in processes.items():
            bin_dict[name] = float(hists[name].GetBinContent(i_bin + 1)) * lumi * cross_section / n_generated_events
        expected.append(bin_dict)
        
        print(f"Adding bin: {expected[-1]})")
    
    data_card = get_datacard_for_signal(expected)
    
    options.out = tmp_combine_file_name
    options.fileName = "./"
    options.verbose = 1
    
    model_builder = CountingModelBuilder(data_card, options)
    model_builder.setPhysics(defaultModel)
    model_builder.doModel()
    

def get_limits_for_signal(signal):
    processes = {
        "ttj": ("ttj.root", n_generated_ttj, cross_section_ttj),
        "ttmumu": ("ttmumu.root", n_generated_ttmumu, cross_section_ttmumu),
        "tta": signal,
    }
    
    print("\n\nPreparing datacard\n\n")
    save_datacard(processes)
    
    print("\n\nRunning combine\n\n")
    os.system(f"combine {tmp_combine_file_name} -M AsymptoticLimits > {tmp_output_file_name}")
    
    print("\n\nReading limits from combine output\n\n")
    limits = {}
    with open(tmp_output_file_name, "r") as file:
        lines = file.readlines()
        
        count = 0
        
        for line in lines:
            if "Expected" in line:
                parts = line.split(" ")
                
                limits[parts[1]] = float(parts[-1])
    
    return limits


def main():
    limits_per_signal = {}

    graph_mean = TGraphAsymmErrors()
    graph_1sigma = TGraphAsymmErrors()
    graph_2sigma = TGraphAsymmErrors()

    graph_mean.SetName("limits_mean")
    graph_1sigma.SetName("limits_1_sigma")
    graph_2sigma.SetName("limits_2_sigma")
    
    i_point = 0
    
    for name, (mass, signal) in signals.items():
        limits_per_signal[name] = get_limits_for_signal(signal)
        
        value = limits_per_signal[name]["50.0%:"]
        up_1_sigma = abs(limits_per_signal[name]["84.0%:"] - value)
        up_2_sigma = abs(limits_per_signal[name]["97.5%:"] - value)
        down_1_sigma = abs(limits_per_signal[name]["16.0%:"] - value)
        down_2_sigma = abs(limits_per_signal[name][""] - value)
        
        graph_mean.SetPoint(i_point, mass, value)
        graph_1sigma.SetPoint(i_point, mass, value)
        graph_1sigma.SetPointError(i_point, 0, 0, down_1_sigma, up_1_sigma)
        graph_2sigma.SetPoint(i_point, mass, value)
        graph_2sigma.SetPointError(i_point, 0, 0, down_2_sigma, up_2_sigma)
        
        i_point += 1

    output_file = TFile(output_file_name, "recreate")
    output_file.cd()

    graph_mean.Write()
    graph_1sigma.Write()
    graph_2sigma.Write()

    output_file.Close()

    print("\n\nSaving limits\n\n")
    print(f"{limits_per_signal=}")
    
    
if __name__ == "__main__":
    main()