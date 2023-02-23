import os
import sys

# Defines input and putput paths to use in the rest of the project
COMMON_OUTPUT_PATH = '/afs/desy.de/user/l/lrygaard/ALPpheno/output_ttalps/' 
COMMON_INPUT_PATH = '/nfs/dust/cms/user/lrygaard/ttalps/inclusive_lhe/'
TDALPS_PATH = './TdAlps/'
MUON_DATA_PATH = '/nfs/dust/cms/user/lrygaard/ttalps/ttj_txt/'

class HiddenPrints:
    """with HiddenPrints(): hides all stdout within this environment"""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
