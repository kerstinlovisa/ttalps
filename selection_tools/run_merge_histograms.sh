#!/bin/bash

process=$1
ctau_option=$2
username=`whoami`

# run as: ./run_merge_histograms process ctau_option
# process:	 ttj / ttmumu       for background
#            tta_mAlp-0p35GeV   for one signal
#            all                for all signals
# ctau_option:	 0 	= default
#		-1 	= reweighted
#		 value 	= ctau in input directory

base_path="/nfs/dust/cms/user/${username}/ttalps"
hadd_path=""
if [ $username == "lrygaard" ]
then
  hadd_path=/afs/desy.de/user/l/lrygaard/tools/miniconda3/envs/tta/bin/hadd
fi
if [ $username == "jniedzie" ]
then
  hadd_path=/afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/hadd
fi

if [ $ctau_option == 0 ]
then
  if [[ $process == "ttj" || $process == "ttmumu" ]]
  then
    base_path="${base_path}/backgrounds/hists"
  else
    base_path="${base_path}/signals_ctau-default/hists"
  fi
else 
  echo $ctau_option
  base_path="${base_path}/signals_ctau-"${ctau_option}"mm/hists"
  ctau_str=()
fi

if [ $ctau_option == 0 ]
then
  if [[ $process == "ttj" ]]
  then
    process="ttj"
    category="muon_siblings"
    $hadd_path -f -j 8 ${base_path}/${category}/${process}.root ${base_path}/${category}/${process}/${process}_part-*
    category="muon_non_siblings"
    $hadd_path -f -j 8 ${base_path}/${category}/${process}.root ${base_path}/${category}/${process}/${process}_part-*
    $hadd_path -f -j 8 ${base_path}/${process}.root ${base_path}/muon_siblings/${process}.root ${base_path}/muon_non_siblings/${process}.root
  fi
  if [[ $process == "ttmumu" ]]
  then
    process="ttmumu"
    category="muon_siblings"
    $hadd_path -f -j 8 ${base_path}/${category}/${process}.root ${base_path}/${category}/${process}/${process}_part-*
    category="muon_non_siblings"
    $hadd_path -f -j 8 ${base_path}/${category}/${process}.root ${base_path}/${category}/${process}/${process}_part-*
    $hadd_path -f -j 8 ${base_path}/${process}.root ${base_path}/muon_siblings/${process}.root ${base_path}/muon_non_siblings/${process}.root
  fi
fi

if [[ $process != "ttj" ]] && [[ $process != "ttmumu" ]]
then

  if [ $process == "all" ]
  then
    processes=("tta_mAlp-0p3GeV" "tta_mAlp-0p35GeV" "tta_mAlp-0p5GeV" "tta_mAlp-0p9GeV" "tta_mAlp-1p25GeV" "tta_mAlp-2GeV" "tta_mAlp-4GeV" "tta_mAlp-8GeV" "tta_mAlp-10GeV")
  else
    processes=($process)
  fi

  for process in ${processes[@]}
  do
    echo $process
    if [ $ctau_option == -1 ]
    then
      category="muon_siblings"
      str=${base_path}/${category}/${process}/${process}_part-0_*
      ctau_str=()
      for s in $str
      do
        ctau=${s: -16:-5}
        ctau_str+=($ctau)
      done

      mkdir ${base_path}/muon_siblings/${process}_ctau/
      mkdir ${base_path}/muon_non_siblings/${process}_ctau/
      mv ${base_path}/muon_siblings/${process}/${process}_part-*mm.root ${base_path}/muon_siblings/${process}_ctau/.
      mv ${base_path}/muon_non_siblings/${process}/${process}_part-*mm.root ${base_path}/muon_non_siblings/${process}_ctau/.
      
      category="muon_siblings"
      str=${base_path}/${category}/${process}_ctau/${process}_part-0_*
      echo $str
      ctau_str=()
      for s in $str
      do
        ctau=${s: -16:-5}
        echo $ctau
        ctau_str+=($ctau)
      done

      for ctau in ${ctau_str[@]}
      do
        category="muon_siblings"
        $hadd_path -f -j 8 ${base_path}/${category}/${process}_ctau-${ctau}.root ${base_path}/${category}/${process}_ctau/*_ctau-${ctau}.root
        category="muon_non_siblings"
        $hadd_path -f -j 8 ${base_path}/${category}/${process}_ctau-${ctau}.root ${base_path}/${category}/${process}_ctau/*_ctau-${ctau}.root

        $hadd_path -f -j 8 ${base_path}/${process}_ctau-${ctau}.root ${base_path}/muon_siblings/${process}_ctau-${ctau}.root ${base_path}/muon_non_siblings/${process}_ctau-${ctau}.root 
      done
    fi

    if [ $ctau_option > 0 ]
    then
      mkdir ${base_path}/muon_siblings/${process}_ctau/
      mkdir ${base_path}/muon_non_siblings/${process}_ctau/
      mv ${base_path}/muon_siblings/${process}/${process}_part-*mm.root ${base_path}/muon_siblings/${process}_ctau/.
      mv ${base_path}/muon_non_siblings/${process}/${process}_part-*mm.root ${base_path}/muon_non_siblings/${process}_ctau/.

      for ctau in ${ctau_str[@]}
      do
        echo $ctau
        category="muon_siblings"
        $hadd_path -f -j 8 ${base_path}/${category}/${process}_ctau-${ctau}.root ${base_path}/${category}/${process}_ctau/*_ctau-${ctau}.root
        category="muon_non_siblings"
        $hadd_path -f -j 8 ${base_path}/${category}/${process}_ctau-${ctau}.root ${base_path}/${category}/${process}_ctau/*_ctau-${ctau}.root

        $hadd_path -f -j 8 ${base_path}/${process}_ctau-${ctau}.root ${base_path}/muon_siblings/${process}_ctau-${ctau}.root ${base_path}/muon_non_siblings/${process}_ctau-${ctau}.root 
      done
    fi

    echo $process
    category="muon_siblings"
    $hadd_path -f -j 8 ${base_path}/${category}/${process}.root ${base_path}/${category}/${process}/${process}_part-*

    category="muon_non_siblings"
    $hadd_path -f -j 8 ${base_path}/${category}/${process}.root ${base_path}/${category}/${process}/${process}_part-*

    $hadd_path -f -j 8 ${base_path}/${process}.root ${base_path}/muon_siblings/${process}.root ${base_path}/muon_non_siblings/${process}.root
  done
fi
