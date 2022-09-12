import os
import sys

COMMON_OUTPUT_PATH = "/home/hd/hd_hd/hd_cu194/ttalps/Output/" # "/home/ruth/Documents/Plots/"
COMMON_INPUT_PATH = "/home/hd/hd_hd/hd_cu194/Samples/ttalps/" #"/home/ruth/Documents/samples/"

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout