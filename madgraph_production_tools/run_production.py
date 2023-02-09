import os
from pathlib import Path
import shutil
import argparse
import fileinput
from math import sqrt, pi
import random
import subprocess

python_path="/afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/python3"
mg_path="/afs/desy.de/user/j/jniedzie/MG5_aMC_v3_4_2/bin/mg5_aMC"
hepmc_path="/afs/desy.de/user/j/jniedzie/hepmc2root/bin/hepmc2root.py"
pythia_path="/afs/desy.de/user/j/jniedzie/MG5_aMC_v3_4_2/HEPTools/pythia8/share/Pythia8/xmldoc"

base_mg_card = "mg5_proc_card_m000050_incl.dat"
base_pythia_card = "pythia8_card.dat"

n_events=100

def remove_existing_files(output_path, file_name):
    command = f"rm -rf {output_path}/{file_name}/"
    print(f"running command: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()


def run_madgraph(config_path):
    command = f"{python_path} {mg_path} {config_path}"
    print(f"running command: {command}")
    os.system(command)


def convert_hepmc_to_root(output_path, file_name):
    hepmc_file_path_original = output_path + "/" + file_name + "/Events/run_01/tag_1_pythia8_events.hepmc.gz"
    hepmc_file_path = output_path + "/" + file_name + "/Events/run_01/"+ file_name +".hepmc.gz"

    command = f"mv {hepmc_file_path_original} {hepmc_file_path}"
    os.system(command)

    command = f"gzip -d {hepmc_file_path}"
    os.system(command)
    
    command = f"{python_path} {hepmc_path} {hepmc_file_path.replace('.gz', '')}"
    os.system(command)


def move_and_cleanup_files(output_path, file_name):
    command = f"mv {file_name}.root {output_path}/"
    os.system(command)
    
    # command = f"mv {output_path}/{file_name}/Events/run_01/unweighted_events.lhe.gz {output_path}/{file_name}.lhe.gz"
    # os.system(command)
    
    command = f"rm -fr {output_path}/{file_name}/"
    os.system(command)


def run_command(config_path, output_path, file_name):
    
    remove_existing_files(output_path, file_name)
    run_madgraph(config_path)
    convert_hepmc_to_root(output_path, file_name)
    move_and_cleanup_files(output_path, file_name)
    
    
def create_paths(paths):
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)

    
def copy_and_update_config(base_config_path, new_config_path, values_to_change):
    
    shutil.copyfile(base_config_path, new_config_path)

    for line in fileinput.input(new_config_path, inplace=True):
        line = line.rstrip()
        if not line:
            continue
        
        for key, value in values_to_change.items():
            keyword, default_value = key
            if keyword in line:
                line = line.replace(default_value, str(value))
        print(line)
        

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", help="", default=0)
    parser.add_argument("-o", "--output_path", help="", default=".")
    
    return parser.parse_args()


def clear_string(s):
    return s.replace(".", "p").replace("-", "m")
    

def main():
    random.seed(None)

    os.system(f"export PYTHIA8DATA={python_path}")
    
    args = get_args()
    part = args.part
    output_path = args.output_path

    create_paths(("tmp_cards", output_path))
    
    file_hash = random.getrandbits(128)
    new_mg_card_path = f"tmp_cards/mg_card_{file_hash}.txt"
    new_pythia_card_path = f"tmp_cards/pythia8_card_{file_hash}.dat"

    file_name = f"tta-0p050GeV"
    file_name += f"_nEvents-{n_events}"
    file_name += f"_part-{part}"

    # prepare MG card
    to_change = {
        ("output", "dummy_value"): output_path+"/"+file_name,
        ("pythia8_card.dat", "pythia8_card.dat"): new_pythia_card_path,
    }

    copy_and_update_config(base_mg_card, new_mg_card_path, to_change)

    # prepare pythia card
    to_change = {
        ("HEPMCoutput:file", "dummy_value"): file_name+".hepmc.gz",
    }

    copy_and_update_config(base_pythia_card, new_pythia_card_path, to_change)

    # run production
    run_command(new_mg_card_path, output_path, file_name)


if __name__ == "__main__":
    main()
