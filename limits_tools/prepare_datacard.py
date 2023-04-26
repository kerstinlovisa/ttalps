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

lumi = 150.0 * 1000.0 # pb-1
lumi_syst = 1.1

n_generated_ttj = 12540000.0
n_generated_ttmumu = 9940000.0

# x_sec in pb
cross_section_ttj = 395.296031
cross_section_ttmumu = 0.02091178

# the empty string includes the default ctau value
#ctaus = ("","0p0000100", "0p0000500", "0p0001000")  # for 1e-4 mm samples
#ctaus = ("","0p1000000", "0p5000000", "1p0000000")  # for 1 mm samples
#ctaus = ("","100p0000000", "50p0000000", "10p0000000")  # for 100 mm samples
ctaus = ("",)  # for 1e5 mm samples

base_path_backgrounds = "/nfs/dust/cms/user/jniedzie/ttalps/hists/"

#base_path = "/nfs/dust/cms/user/lrygaard/ttalps/hists/"
#base_path = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-1em4mm/hists/"
#base_path = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-1mm/hists/"
#base_path = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-1e2mm/hists/"
#base_path = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-1e2mm_test_pTcut5/hists/"
#base_path = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-1e2mm_test_func/hists/"
base_path = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-1e5mm/hists/"

#base_path = "/nfs/dust/cms/user/jniedzie/ttalps/hists/"


# 1e-4 mm samples
#signals = {
#                           mass     file                       n_gen       ref. x_sec (pb)
#        "tta_mAlp-0p2GeV":    (0.2,   (base_path+"tta_mAlp-0p2GeV.root",    823515.0, 1e-3)),
#        "tta_mAlp-0p3GeV":    (0.3,   (base_path+"tta_mAlp-0p3GeV.root",    794059.0, 1e-3)),
#        "tta_mAlp-0p35GeV":   (0.35,  (base_path+"tta_mAlp-0p35GeV.root",   811341.0, 1e-3)),
#        "tta_mAlp-0p5GeV":    (0.5,   (base_path+"tta_mAlp-0p5GeV.root",    819359.0, 1e-3)),
#        "tta_mAlp-0p9GeV":    (0.9,   (base_path+"tta_mAlp-0p9GeV.root",    889230.0, 1e-3)),
#        "tta_mAlp-1p25GeV":   (1.25,  (base_path+"tta_mAlp-1p25GeV.root",   798418.0, 1e-3)),
#        "tta_mAlp-2GeV":      (2.0,   (base_path+"tta_mAlp-2GeV.root",      897726.0, 1e-3)),
#        "tta_mAlp-4GeV":      (4.0,   (base_path+"tta_mAlp-4GeV.root",      857528.0, 1e-3)),
#        "tta_mAlp-8GeV":      (8.0,   (base_path+"tta_mAlp-8GeV.root",      920562.0, 1e-3)),
#        "tta_mAlp-10GeV":     (10,    (base_path+"tta_mAlp-10GeV.root",     864471.0, 1e-3)),
#}

# 1 mm samples
#signals = {
#                           mass     file                       n_gen      ref. x_sec (pb)
#	"tta_mAlp-0p2GeV":	(0.2,   (base_path+"tta_mAlp-0p2GeV.root",    980000.0, 1e-3)),
#	"tta_mAlp-0p3GeV":      (0.3,   (base_path+"tta_mAlp-0p3GeV.root",    990000.0, 1e-3)),
#	"tta_mAlp-0p35GeV":     (0.35,  (base_path+"tta_mAlp-0p35GeV.root",   990000.0, 1e-3)),
#	"tta_mAlp-0p5GeV":      (0.5,   (base_path+"tta_mAlp-0p5GeV.root",    1000000.0, 1e-3)),
#	"tta_mAlp-0p9GeV":      (0.9,   (base_path+"tta_mAlp-0p9GeV.root",    990000.0, 1e-3)),
#	"tta_mAlp-1p25GeV":     (1.25,  (base_path+"tta_mAlp-1p25GeV.root",   980000.0, 1e-3)),
#	"tta_mAlp-2GeV":        (2.0,   (base_path+"tta_mAlp-2GeV.root",      1000000.0, 1e-3)),
#	"tta_mAlp-4GeV":        (4.0,   (base_path+"tta_mAlp-4GeV.root",      1000000.0, 1e-3)),
#	"tta_mAlp-8GeV":        (8.0,   (base_path+"tta_mAlp-8GeV.root",      1000000.0, 1e-3)),
#	"tta_mAlp-10GeV":       (10,    (base_path+"tta_mAlp-10GeV.root",     980000.0, 1e-3)),
#}

# 100 mm samples
#signals = {
#                           mass     file                       n_gen       ref. x_sec (pb)
#    	"tta_mAlp-0p2GeV":	(0.2,   (base_path+"tta_mAlp-0p2GeV.root",    945666.0, 1e-3)),
#        "tta_mAlp-0p3GeV":	(0.3,   (base_path+"tta_mAlp-0p3GeV.root",    939472.0, 1e-3)),
#        "tta_mAlp-0p35GeV":     (0.35,  (base_path+"tta_mAlp-0p35GeV.root",   954548.0, 1e-3)),
#        "tta_mAlp-0p5GeV":	(0.5,   (base_path+"tta_mAlp-0p5GeV.root",    910031.0, 1e-3)),
#        "tta_mAlp-0p9GeV":	(0.9,   (base_path+"tta_mAlp-0p9GeV.root",    905981.0, 1e-3)),
#        "tta_mAlp-1p25GeV":	(1.25,  (base_path+"tta_mAlp-1p25GeV.root",   904457.0, 1e-3)),
#        "tta_mAlp-2GeV":	(2.0,   (base_path+"tta_mAlp-2GeV.root",      902781.0, 1e-3)),
#        "tta_mAlp-4GeV":	(4.0,   (base_path+"tta_mAlp-4GeV.root",      957228.0, 1e-3)),
#        "tta_mAlp-8GeV":	(8.0,   (base_path+"tta_mAlp-8GeV.root",      881900.0, 1e-3)),
#        "tta_mAlp-10GeV":	(10,    (base_path+"tta_mAlp-10GeV.root",     959596.0, 1e-3)),
#}

# 1e5 mm samples
signals = {
    #                           mass     file                       n_gen       ref. x_sec (pb)
    #	"tta_mAlp-0p2GeV":    (0.2,   (base_path+"tta_mAlp-0p2GeV.root",    824599.0, 1e-3)),
#    "tta_mAlp-0p3GeV":    (0.3,   (base_path+"tta_mAlp-0p3GeV.root",    617049.0, 1e-3)),
    "tta_mAlp-0p35GeV":   (0.35,  (base_path+"tta_mAlp-0p35GeV.root",   600727.0, 1e3)),
    "tta_mAlp-0p5GeV":    (0.5,   (base_path+"tta_mAlp-0p5GeV.root",    634373.0, 1e3)),
    "tta_mAlp-0p9GeV":    (0.9,   (base_path+"tta_mAlp-0p9GeV.root",    566575.0, 1e3)),
    "tta_mAlp-1p25GeV":   (1.25,  (base_path+"tta_mAlp-1p25GeV.root",   495886.0, 1e3)),
    "tta_mAlp-2GeV":      (2.0,   (base_path+"tta_mAlp-2GeV.root",      551414.0, 1e3)),
    "tta_mAlp-4GeV":      (4.0,   (base_path+"tta_mAlp-4GeV.root",      543955.0, 1e-3)),
    "tta_mAlp-8GeV":      (8.0,   (base_path+"tta_mAlp-8GeV.root",      494375.0, 1e-3)),
    "tta_mAlp-10GeV":     (10,    (base_path+"tta_mAlp-10GeV.root",     620215.0, 1e-3)),
}


#cuts = "mass-cuts"
#cuts = "mass-cuts_dR-0p1"
#cuts = "mass-cuts_dR-0p2"
#cuts = "pt-10GeV_dR-0p1"
#cuts = "pt-10GeV_dR-0p2"
#cuts = "pt-10GeV_mass-cuts_dR-0p1"
#cuts = "pt-10GeV_mass-cuts_dR-0p2"
#cuts = "pt-10GeV_mass-cuts"
#cuts = "pt-5GeV_dR-0p1"
#cuts = "pt-5GeV_dR-0p2"
#cuts = "pt-5GeV_mass-cuts_dR-0p1"
#cuts = "pt-5GeV_mass-cuts_dR-0p2"
#cuts = "pt-5GeV_mass-cuts"

cuts = "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1"

hist_name = f"final_selection/final_selection_{cuts}_os_maxlxy-muon_lxy_rebinned"
output_file_name = f"limits_{cuts}.root"

tmp_combine_file_name = "tmp_combine_workspace.root"
tmp_output_file_name = "tmp_output.txt"

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
        files[name] = TFile.Open(input_file_name)
        hists[name] = files[name].Get(hist_name)

        if not files[name] or not hists[name]:
            print(f"couldn't open hist: {hist_name} from file: {input_file_name}")

        n_bins = hists[name].GetNbinsX()
    
    expected = []
    
    for i_bin in range(n_bins):
        bin_dict = {}
        for name, (_, n_generated_events, cross_section) in processes.items():
            bin_dict[name] = float(hists[name].GetBinContent(i_bin + 1)) * lumi * cross_section / n_generated_events
            
        if bin_dict["tta"] == 0:
            bin_dict["tta"] = 1e-50
        
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
        "ttj": (base_path_backgrounds+"ttj.root", n_generated_ttj, cross_section_ttj),
        "ttmumu": (base_path_backgrounds+"ttmumu.root", n_generated_ttmumu, cross_section_ttmumu),
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

        for line in lines:
            if "Expected" in line:
                parts = line.split(" ")
                limits[parts[1]] = float(parts[-1])
    
    return limits


def main():
    print("\n\nSaving limits\n\n")
    output_file = TFile(output_file_name, "recreate")
    output_file.cd()

    for ctau in ctaus:

        limits_per_signal = {}

        ctau_name = "" if ctau=="" else f"_ctau-{ctau}mm"

        graph_mean = TGraphAsymmErrors()
        graph_1sigma = TGraphAsymmErrors()
        graph_2sigma = TGraphAsymmErrors()

        graph_mean.SetName(f"limits_mean{ctau_name}")
        graph_1sigma.SetName(f"limits_1_sigma{ctau_name}")
        graph_2sigma.SetName(f"limits_2_sigma{ctau_name}")
    
        i_point = 0

        for name, (mass, signal) in signals.items():

            updated_signal = list(signal)
 
            if ctau != "":
                updated_signal[0] = updated_signal[0].replace(".root", f"{ctau_name}.root")

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
