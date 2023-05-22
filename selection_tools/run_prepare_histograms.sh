#!/bin/bash

process=$1
part=$2
input_user=$3
ctau_option=$4
username=`whoami`

base_input_path="/nfs/dust/cms/user/${input_user}/ttalps"
base_output_path="/nfs/dust/cms/user/${username}/ttalps"
output_file_name="${process}_part-${part}.root"

if [ $ctau_option == 0 ]
then 
  if [[ $process == "ttj" || $process == "ttmumu" ]]
  then
    base_output_path="${base_output_path}/backgrounds"
    # base_output_path="${base_output_path}/backgrounds_non-prompt-selection"
    # base_output_path="${base_output_path}/backgrounds_non-muon-mothers"
    base_input_path="${base_input_path}/backgrounds_non-muon-mothers"
  else
    # base_output_path="${base_output_path}/signals_ctau-default"
    base_output_path="${base_output_path}/signals_default_ptAlp-ge5GeV"
    # base_output_path="${base_output_path}/signals_ctau-default_muon-status"
    # base_output_path="${base_output_path}/signals_ctau-default_non-muon-mothers"
    # base_input_path="${base_input_path}/signals_ctau-default_non-muon-mothers"
    base_input_path="${base_input_path}/signals_default_ptAlp-ge5GeV"
    # base_output_path="${base_output_path}/signals_ctau-default"
    # base_input_path="${base_input_path}/signals_ctau-default"
  fi
else
  base_output_path="${base_output_path}/signals_ctau-${ctau_option}mm"
  base_input_path="${base_input_path}/signals_ctau-${ctau_option}mm"
fi

category="muon_siblings"
input_path=`ls ${base_input_path}/after_preselection/${category}/${process}/*root -1 | sed -n $((part+1))p`
output_path="${base_output_path}/hists/${category}/${process}"
mkdir -p $output_path
echo $input_path "  >>  " $output_path
./prepare_histograms $input_path $output_path/$output_file_name $ctau_option

category="muon_non_siblings"
input_path=`ls ${base_input_path}/after_preselection/${category}/${process}/*root -1 | sed -n $((part+1))p`
output_path="${base_output_path}/hists/${category}/${process}"
mkdir -p $output_path
echo $input_path "  >>  " $output_path
./prepare_histograms $input_path $output_path/$output_file_name $ctau_option
