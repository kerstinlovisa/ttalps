import os
import math
from pathlib import Path
import shutil
import argparse
import fileinput
from math import sqrt, pi
import random
import subprocess
#import physics as ph

python_path = "/afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/python3"
mg_path = "/afs/desy.de/user/j/jniedzie/MG5_aMC_v3_4_2/bin/mg5_aMC"
#hepmc_path = "/afs/desy.de/user/j/jniedzie/hepmc2root/bin/hepmc2root.py"
hepmc_path = "/afs/desy.de/user/j/jniedzie/ttalps/ttalps/external_tools/hepmc2root/hepmc2root"
pythia_path = "/afs/desy.de/user/j/jniedzie/MG5_aMC_v3_4_2/HEPTools/pythia8/share/Pythia8/xmldoc"

base_pythia_card = "pythia8_card.dat"

keep_lhe = False


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
    #command += f"{python_path} {hepmc_path} {file_name}.hepmc"
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
#    move_and_cleanup_files(output_path, file_name)
    
    
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


def getLSfromctt(ctL,ctR, Lambda, mu):
    """Returns low-energy coefficient dictionary from UV ALP-top couplings
    
    Interface function to the TdAlps package
    ctL - coupling of the lefthanded top-quark to the ALP in the UV
    ctR - coupling of the righthanded top-quark to the ALP in the UV
    Lambda - cutoff scale of the ALP-EFT where ctL and ctR are defines
    mu - low-energy scale to which the couplings are run
    the running is based on hep-ph: [2012.12272]"""
    with aux.HiddenPrints():
        HC = OrderedDict()
        HC['Q'] = np.array([[0,0,0],[0,0,0],[0,0,-ctL]])
        HC['u'] = np.array([[0,0,0],[0,0,0],[0,0,ctR]])
        HC['d'] = np.array([[0,0,0],[0,0,0],[0,0,0]])
        HC['L'] = np.array([[0,0,0],[0,0,0],[0,0,0]])
        HC['e'] = np.array([[0,0,0],[0,0,0],[0,0,0]])
        HC['GG'] = 0
        HC['WW'] = 0
        HC['BB'] = 0
        if mu<1:
            mu=1
    return TdAlps.RunRotateMatchRun(HC, Lambda, mu, 3)


sm={
    'sw': math.sqrt(0.23121), # sin(theta_weak)
    'hbar': 6.582119569*10**(-25), # h/2pi in GeVs
    'c': 29979245800, # speed of light in cm/s
    'me': 0.0005109989461, # eletron mass in GeV
    'mmu': 0.1056583745, # muon mass in GeV
    'mtau': 1.77686, # tauon mass in GeV
    'mu': 0.00216, # up quark mass in GeV
    'md': 0.00467, # down quark mass in GeV
    'ms': 0.093, # strange quark mass in GeV
    'mc': 1.27, #charm quark mass in GeV
    'mb': 4.18, # bottom quark mass in GeV
    'mt': 163.6, # top quark mass in GeV
    'mZ': 91.1876, # Z boson mass in GeV
    'mB+': 5.27934, # charged B meson mass in GeV
    'mK+': 0.493677, # charged kaon mass in GeV
    'mpi+': 0.13957039, # charged pion mass in GeV
    'mpi0': 0.1349768, # neutral pion mass in GeV
    'fpi': 0.130, # pion decay constant
    'tauB+': 1.638*10**(-12), # charged B meson lifetime in s
    'GF': 1.166*10**(-5), # Fermi constant
    'alpha': 1/137, # electromagnetic coupling 
    'Vtb': 0.999, # absolute value of CKM element tb
    'Vts': 0.0404, # absolute value of CKM element ts
    'Xt': 1.462, # effective B->Knunu vertex coupling from [1409.4557]
    'BrBtoKnunu+': 4.5*10**(-6), # Branching ratio of B->K nu nu decay
    'NBBBaBar': 471*10**6, # number of BB pairs produced at BaBar
    'NBBBelleII': 5*10**10, # number of BB pairs produced at Belle II
    'mp': 0.9383, # proton mass in GeV
    'mn': 0.9396 # neutron mass in GeV
}


def Gammaatoll(ma, cll, ml, Lambda):
    """decay rate of an ALP to a pair of leptons
    
    ma - ALP mass
    cll - coupling of ALP to leptons
    ml - mass of leptons
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    if ma <= 2 * ml:
        return 0
    gamma = ml**2 * abs(cll)**2 * math.sqrt(ma**2 - 4 * ml**2) * 2 * math.pi / (Lambda**2) 
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to leptons with mass " + str(ml) + " is complex: " + str(gamma))
    return float(gamma)

def Gammaatoqq(ma, cqq, mq, Lambda):
    """decay rate of an ALP to a pair of quarks
    
    ma - ALP mass
    cqq - coupling of ALP to quarks
    mq - mass of leptons
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    if ma <= 2 * mq:
        return 0
    gamma = 3 * mq**2 * abs(cqq)**2 * math.sqrt(ma**2 - 4 * mq**2) * 2 * math.pi / (Lambda**2) 
    if gamma.imag  != 0:
        if gamma.imag/gamma.real > 10**-10:
            print("The Decay rate to quarks with mass " + str(mq) + " is complex: " + str(gamma))
    return float(gamma)


def Gammaa(ma, ctL, ctR, Lambda):
    """Decay rate of the ALP as induced only by top couplings
    
    ma - ALP mass
    ctL - coupling of the lefthanded top-quark to the ALP in the UV
    ctR - coupling of the righthanded top-quark to the ALP in the UV
    Lambda - cutoff scale of the ALP-EFT
    following hep-ph: [2012.12272]"""
    lscs = getLSfromctt(ctL,ctR, Lambda, ma)
    GammaTot = 0
    if ma>2*sm['me']:
        GammaTot += Gammaatoll(ma,readCee(lscs),sm['me'],Lambda)
    if ma>2*sm['mmu']:
        GammaTot += Gammaatoll(ma,readCmumu(lscs),sm['mmu'],Lambda)
    if ma>2*sm['mtau']:
        GammaTot += Gammaatoll(ma,readCtautau(lscs),sm['mtau'],Lambda)
    if ma>2*sm['mc']:
        GammaTot += Gammaatoqq(ma,readCcc(lscs),sm['mc'],Lambda)
    if ma>2*sm['mb']:
        GammaTot += Gammaatoqq(ma,readCbb(lscs),sm['mb'],Lambda)
    if ma>1:
        GammaTot += Gammaatohad(ma,lscs,Lambda)
    if ma<2:
        GammaTot += Gammaato3pi0pm(ma,lscs,Lambda)
        GammaTot += Gammaato3pi000(ma,lscs,Lambda)
    GammaTot += Gammaatogamgam(ma,lscs,Lambda)
    

def main():
    random.seed(None)

    os.system(f"export PYTHIA8DATA={python_path}")
    
    args = get_args()
    output_path = args.output_path

    create_paths(("tmp_cards", output_path))
    
    file_hash = random.getrandbits(128)
    new_mg_card_path = f"tmp_cards/mg_card_{file_hash}.txt"
    new_pythia_card_path = f"tmp_cards/pythia8_card_{file_hash}.dat"

    process = args.process

    file_name = get_output_file_name(process, args.part, args.n_events, args.alp_mass)

    # prepare MG card
    to_change = {
        ("output", "dummy_value"): output_path+"/"+file_name,
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

    alp_mass = float(args.alp_mass)
#    ctau = ph.ctaua(alp_mass, 0.5, -0.5, 1000)
#    tau = ctau / 29979245800
#    gamma = 6.582119569*10**(-25) / tau

    tau = 1e-5
    gamma = 1e-20

    to_change = {
        ("HEPMCoutput:file", "dummy_value"): file_name+".hepmc.gz",

	("ParticleData:addParticle", "dummy_mass"): alp_mass,
	("ParticleData:addParticle", "dummy_width"): gamma,
	("ParticleData:addParticle", "dummy_mMin"): alp_mass - gamma,
 	("ParticleData:addParticle", "dummy_mMax"): alp_mass + gamma,
	("ParticleData:addParticle", "dummy_tau"): tau,
    }

    copy_and_update_config(base_pythia_card, new_pythia_card_path, to_change)

    # run production
    run_command(new_mg_card_path, output_path, file_name)


if __name__ == "__main__":
    main()
