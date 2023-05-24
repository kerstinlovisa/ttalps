#!/bin/bash


__set_conda() {
    conda activate $1
}

__set_pythonpath() {
    local analysis_dir=$1
    export PYTHONPATH="${analysis_dir}/"
    export PYTHONPATH="${PYTHONPATH}:${analysis_dir}/TdAlps/"
    export PYTHONPATH="${PYTHONPATH}:${analysis_dir}/limits_tools/"
}


if [ "$1" == "condor" ]; then
    __set_pythonpath $2
else
    __set_conda tta
    __set_pythonpath ${PWD}
fi
