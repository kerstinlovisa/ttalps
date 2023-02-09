#!/bin/bash

user_base_path="/afs/desy.de/user/j/jniedzie/ttalps/ttalps/mg_production/"
output_path="/nfs/dust/cms/user/jniedzie/ttalps/"
python_path="/afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/python3"

export PYTHIA8DATA=/afs/desy.de/user/j/jniedzie/MG5_aMC_v3_4_2/HEPTools/pythia8/share/Pythia8/xmldoc

#conda init bash
#conda activate llp

# source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.12.06/x86_64-centos7-gcc48-opt/root/bin/thisroot.sh

cd $user_base_path || exit
#mkdir -p output error log

$python_path $user_base_path/run_production.py -p $1 -o $output_path
