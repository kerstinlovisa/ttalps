#!/bin/bash


__set_conda() {
    conda activate $1
}

__set_pythonpath() {
    local svj_analysis_dir=$1
    export PYTHONPATH="${svj_analysis_dir}/"
    export PYTHONPATH="${PYTHONPATH}:${svj_analysis_dir}/TdAlps/"
}


if [ "$1" == "condor" ]; then
    __set_pythonpath $2
else
    __set_conda tta
    __set_pythonpath ${PWD}
fi
