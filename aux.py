import os
import sys

COMMON_OUTPUT_PATH = "/home/ruth/Documents/Plots/" #"/home/ruth/Seafile/TTALP/RuthPlots/"
COMMON_INPUT_PATH = "/home/ruth/Documents/lhe_files/" #"/home/ruth/Seafile/TTALP/lhe_files/"

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout