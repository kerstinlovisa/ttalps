#!/bin/bash

file_name="ttj_nEvents-10000_nDaughters-100_part-0.root"
input_path="/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/gen_level/"
single_muon_output_path="/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/after_selections/single_muon/"
muon_pair_output_path="/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/after_selections/muon_siblings/"
muon_non_pair_output_path="/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/after_selections/muon_non_siblings/"

./apply_selections $file_name $input_path $single_muon_output_path $muon_pair_output_path $muon_non_pair_output_path
