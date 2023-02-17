#!/bin/bash

process=$1
part=$2

base_output_path="/nfs/dust/cms/user/jniedzie/ttalps"
output_file_name="${process}_part-${part}.root"

category="single_muon"
input_path=`ls ${base_output_path}/after_preselection/${category}/${process}/*root -1 | sed -n $((part+1))p`
output_path="${base_output_path}/hists/${category}/${process}/"
./prepare_histograms $input_path $output_path

category="muon_siblings"
input_path=`ls ${base_output_path}/after_preselection/${category}/${process}/*root -1 | sed -n $((part+1))p`
output_path="${base_output_path}/hists/${category}/${process}/"
./prepare_histograms $input_path $output_path

category="muon_non_siblings"
input_path=`ls ${base_output_path}/after_preselection/${category}/${process}/*root -1 | sed -n $((part+1))p`
output_path="${base_output_path}/hists/${category}/${process}/"
./prepare_histograms $input_path $output_path
