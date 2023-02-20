from glob import glob
import argparse

from ROOT import TFile, TTree


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path')
    args = parser.parse_args()
    
    path = args.path
    files = glob(path)
    
    n_events=0

    for file_name in files:
        file = TFile.Open(file_name)
        if not file:
            continue
        tree = file.Get("Events")
        
        if not tree:
            continue
            
        n_events += tree.GetEntries()
        
    print(f"Total number of events in {len(files)}: {n_events}")


if __name__ == "__main__":
    main()