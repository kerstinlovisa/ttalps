#!/bin/bash

process=$1
part=$2

base_output_path="/nfs/dust/cms/user/jniedzie/ttalps"

input_file_path=`ls ${base_output_path}/${process}_nEvents-10000*/*root -1 | sed -n $((part+1))p`

input_path=$(dirname "$input_file_path")
input_path="${input_path}/"
file_name=$(basename "$input_file_path")

output_file_name="${process}_part-${part}.root"

single_muon_output_path="${base_output_path}/after_preselection/single_muon/${process}/"
muon_pair_output_path="${base_output_path}/after_preselection/muon_siblings/${process}/"
muon_non_pair_output_path="${base_output_path}/after_preselection/muon_non_siblings/${process}/"

echo "file name: ${file_name}"
echo "input path: ${input_path}"
echo "output path: ${single_muon_output_path}, ${muon_pair_output_path}, ${muon_non_pair_output_path}"
echo "output file: ${output_file_name}"

./apply_selections $file_name $input_path $output_file_name $single_muon_output_path $muon_pair_output_path $muon_non_pair_output_path
