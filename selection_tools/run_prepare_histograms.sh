#!/bin/bash

process=$1
part=$2
input_user=$3
username=`whoami`

base_input_path="/nfs/dust/cms/user/${input_user}/ttalps"
base_output_path="/nfs/dust/cms/user/${username}/ttalps"
output_file_name="${process}_part-${part}.root"

category="muon_siblings"
input_path=`ls ${base_input_path}/after_preselection/${category}/${process}/*root -1 | sed -n $((part+1))p`
output_path="${base_output_path}/hists/${category}/${process}"
mkdir -p $output_path
./prepare_histograms $input_path $output_path/$output_file_name

category="muon_non_siblings"
input_path=`ls ${base_input_path}/after_preselection/${category}/${process}/*root -1 | sed -n $((part+1))p`
output_path="${base_output_path}/hists/${category}/${process}"
mkdir -p $output_path
./prepare_histograms $input_path $output_path/$output_file_name
