#!/bin/bash

username=`whoami`
firstletter=${username:0:1}


if [ $username == "jniedzie" ]
  then
  user_base_path="/afs/desy.de/user/${firstletter}/${username}/ttalps/ttalps/madgraph_production_tools/"
  python_path="/afs/desy.de/user/${firstletter}/${username}/miniconda3/envs/tta/bin/python3"

  #output_path="/nfs/dust/cms/user/jniedzie/ttalps"
  #output_path="/nfs/dust/cms/user/jniedzie/ttalps/signals_ctau-1mm"
  #output_path="/nfs/dust/cms/user/jniedzie/ttalps/signals_ctau-1e2mm"
  output_path="/nfs/dust/cms/user/jniedzie/ttalps/signals_ctau-1em4mm"

  export PYTHIA8DATA=/afs/desy.de/user/${firstletter}/${username}/MG5_aMC_v3_4_2/HEPTools/pythia8/share/Pythia8/xmldoc
else
  if [ $username == "lrygaard" ]
  then  
    user_base_path="/afs/desy.de/user/${firstletter}/${username}/ALPpheno/ttalps/madgraph_production_tools/"
    output_path="/nfs/dust/cms/user/${username}/ttalps/"
    python_path="/afs/desy.de/user/${firstletter}/${username}/tools/miniconda3/envs/tta/bin/python3"

    export PYTHIA8DATA=/afs/desy.de/user/${firstletter}/${username}/tools/MG5_aMC_v3_4_2/HEPTools/pythia8/share/Pythia8/xmldoc
  else
    echo "Error username unknown"
  fi
fi

cd $user_base_path || exit

$python_path $user_base_path/run_production.py -pr $1 -p $2 -n $3 -m $4 -o $output_path -l $5
