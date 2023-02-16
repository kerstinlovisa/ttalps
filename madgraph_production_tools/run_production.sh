#!/bin/bash

user_base_path="/afs/desy.de/user/j/jniedzie/ttalps/ttalps/madgraph_production_tools/"
output_path="/nfs/dust/cms/user/jniedzie/ttalps/"
python_path="/afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/python3"

export PYTHIA8DATA=/afs/desy.de/user/j/jniedzie/MG5_aMC_v3_4_2/HEPTools/pythia8/share/Pythia8/xmldoc

cd $user_base_path || exit

$python_path $user_base_path/run_production.py -pr $1 -p $2 -n $3 -m $4 -o $output_path
