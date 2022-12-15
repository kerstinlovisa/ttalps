import os
import sys

# Defines input and putput paths to use in the rest of the project
COMMON_OUTPUT_PATH = '/eos/user/l/lrygaard/ttalp/output/' #"/home/hd/hd_hd/hd_cu194/ttalps/Output/" # "/home/ruth/Documents/Plots/"
COMMON_INPUT_PATH = '/eos/user/j/jalimena/TTALP/lhe_files/' # "/home/hd/hd_hd/hd_cu194/Samples/ttalps/" #"/home/ruth/Documents/samples/"
TDALPS_PATH = '/afs/cern.ch/user/l/lrygaard/private/ALPpheno/TdAlps/'
MUON_DATA_PATH = '/afs/cern.ch/user/l/lrygaard/private/madanalysis5/ALPanalysis/Output/TXT/ttj100000/'

class HiddenPrints:
    """with HiddenPrints(): hides all stdout within this environment"""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
