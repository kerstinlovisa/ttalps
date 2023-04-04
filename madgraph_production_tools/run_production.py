import os
import math
from pathlib import Path
import shutil
import argparse
import fileinput
from math import sqrt, pi
import random
import subprocess
import physics as ph

python_path = "/afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/python3"
mg_path = "/afs/desy.de/user/j/jniedzie/MG5_aMC_v3_4_2/bin/mg5_aMC"
hepmc_path = "/afs/desy.de/user/j/jniedzie/ttalps/ttalps/external_tools/hepmc2root/hepmc2root"
pythia_path = "/afs/desy.de/user/j/jniedzie/MG5_aMC_v3_4_2/HEPTools/pythia8/share/Pythia8/xmldoc"

base_pythia_card = "pythia8_card.dat"
base_param_card = "param_card.dat"

keep_lhe = False
use_gamma_total = False
Lambda = 4*math.pi*1000
coupling = 0.5

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
    hepmc_file_path = output_path + "/" + file_name + "/Events/run_01/" + file_name + ".hepmc.gz"

    command = f"mv {hepmc_file_path_original} {hepmc_file_path}"
    os.system(command)

    command = f"cd {output_path}/{file_name}/Events/run_01/;"
    command += f"gzip -d {file_name}.hepmc.gz"
    os.system(command)
    
    command = f"cd {output_path}/{file_name}/Events/run_01/;"
    command += f"{hepmc_path} {file_name}.hepmc"
    os.system(command)


def move_and_cleanup_files(output_path, file_name):
    
    output_dir_name = "_".join(file_name.split("_")[0:-1])
    
    command = f"mkdir -p {output_path}/{output_dir_name}"
    os.system(command)
    
    command = f"mv {output_path}/{file_name}/Events/run_01/{file_name}.root {output_path}/{output_dir_name}/"
    os.system(command)
    
    if keep_lhe:
        command = f"mv {output_path}/{file_name}/Events/run_01/unweighted_events.lhe.gz "
        command += f"{output_path}/{output_dir_name}/{file_name}.lhe.gz"
        os.system(command)
    
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
    parser.add_argument("-n", "--n_events", help="", default=100)
    parser.add_argument("-m", "--alp_mass", help="", default=50e-03)
    parser.add_argument("-o", "--output_path", help="", default=".")
    parser.add_argument("-pr", "--process", help="", default="tta")
    
    return parser.parse_args()


def clear_string(s):
    return s.replace(".", "p").replace("-", "m")
    

def get_output_file_name(process, part, n_events, alp_mass):
    alp_mass_name = clear_string(f"{alp_mass}")
    
    file_name = f"{process}"
    
    if process == "tta":
        file_name += f"_mAlp-{alp_mass_name}GeV"
    file_name += f"_nEvents-{n_events}"
    file_name += f"_part-{part}"
    
    return file_name


def main():
    random.seed(None)

    os.system(f"export PYTHIA8DATA={python_path}")
    
    args = get_args()
    output_path = args.output_path

    create_paths(("tmp_cards", output_path))
    
    file_hash = random.getrandbits(128)
    new_mg_card_path = f"tmp_cards/mg_card_{file_hash}.txt"
    new_pythia_card_path = f"tmp_cards/pythia8_card_{file_hash}.dat"
    new_param_card_path = f"tmp_cards/param_card_{file_hash}.dat"

    process = args.process

    file_name = get_output_file_name(process, args.part, args.n_events, args.alp_mass)

    # prepare MG card
    to_change = {
        ("output", "dummy_value"): output_path+"/"+file_name,
        ("param_card.dat", "param_card.dat"): new_param_card_path,
        ("pythia8_card.dat", "pythia8_card.dat"): new_pythia_card_path,
        ("set Ma", "dummy_value"): args.alp_mass,
        ("set nevents", "dummy_value"): args.n_events,
        ("set iseed", "dummy_value"): random.randint(0, 900000000),
    }

    base_mg_card = None

    if process == "tta":
        base_mg_card = "mg5_card_tta.dat"
    elif process == "ttj":
        base_mg_card = "mg5_card_ttj.dat"
    elif process == "ttmumu":
        base_mg_card = "mg5_card_ttmumu.dat"
    else:
        print(f"\n\nERROR -- unrecognized process: {process}")
        exit(0)

    copy_and_update_config(base_mg_card, new_mg_card_path, to_change)

    # prepare pythia card
    to_change = {
        ("HEPMCoutput:file", "dummy_value"): file_name+".hepmc.gz",
    }

    copy_and_update_config(base_pythia_card, new_pythia_card_path, to_change)

    # prepare param card
    alp_mass = float(args.alp_mass)
    
    if use_gamma_total:
        gamma = ph.Gammaa(alp_mass, coupling, coupling, Lambda)
    else:
        lscs = ph.getLSfromctt(coupling, coupling, Lambda, alp_mass)
        gamma = ph.Gammaatoll(alp_mass, ph.readCmumu(lscs), ph.sm['mmu'], Lambda)
    
    to_change = {
        ("# ma", "dummy_value"): alp_mass,
        ("# ax", "dummy_value"): gamma,
    }

    copy_and_update_config(base_param_card, new_param_card_path, to_change)

    # run production
    run_command(new_mg_card_path, output_path, file_name)


if __name__ == "__main__":
    main()
