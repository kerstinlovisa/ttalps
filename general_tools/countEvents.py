from glob import glob
import argparse

from ROOT import TFile, TTree

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path')
    args = parser.parse_args()
    
    path = args.path
    files = glob(path)
    
    n_events=0
    n_files = len(files)

    for i_file, file_name in enumerate(files):
        printProgressBar(i_file + 1, n_files, prefix = 'Progress:', suffix = 'Complete', length = 50)
#        print(f"{i_file}/{n_files}")

        try:
            file = TFile.Open(file_name)
        except OSError:
            continue

        if not file:
            continue
        tree = file.Get("Events")
        
        if not tree:
            continue
            
        n_events += tree.GetEntries()
        
    print(f"Total number of events in {len(files)}: {n_events}")


if __name__ == "__main__":
    main()
