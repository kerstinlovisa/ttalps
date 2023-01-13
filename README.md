# ttalps

This GitLab repository contains the code so far accumulated in the exploration of signatures of ALPs produced together with a top antitop pair at the CMS detector at the LHC, with the ALP decaying into a muon pair. We use this code to compare the signatures of signal events (tta->ttmumu) with background events which do not have an ALP (ttmumu) to separate the two sets of events on the basis of their kinematic variables.

## Setup of virtual invironment

For running the code with all necessary libraries, run with python3 venv as:
`python3 -m venv ttalps` 
For invironment name ttalps, in the ttalps directory.
`source bin/activate`
`pip install -r requirements.txt`
To deactivate `deactive`.

## Structure of the code

The code is made up of four auxiliary python files:
- The file `aux.py` contains the input and output paths used in all Jupyter notebooks as well as the HiddenPrints context manager.
- The file `data_classes.py` contains the definitions of the classes for `FourVector`, `FourMomentum`, `Particle`, `Event`, and `Dataset` which we encapsulate our data in. They contain many useful methods for calculating observables.
- The file `myplot.py` contains convenient shortcuts to plots we use, as well as their colour scheme and a dictionary of commonly used labels for plot axes, `dirLabels`, for consistency.
- The file `physics.py` contains the used interface to `TdAlps`, functions for the calculation of lifetimes and branching ratios, as well as a dictionary of the physical constants needed, `sm`.

The package `TdAlps` used here comes from the Github repository https://github.com/TdAlps/TdAlps and is based on the paper hep-ph:[2012:12272] which describes Lagrangian we use and its RG-evolution. The package allows for the running of couplings in the ALP model we use.

We use these .py-files in the Jupyter notebooks:
- `Decays.ipynb` explores the ALPs lifetime and branching ratio in the considered coupling setup
- `Data_Exploration.ipynb` works with the samples to explore the generated events' parameter space
- `dc_tests.ipynb` is used to test the classes and methods of dataclasses.py with a reduced dataset


The folder `MadAnalysis` contains `.cpp` and `.h` files that are scripts for the program `MadAnalysis5` which is used here to convert `.hepmc` files with generated events to `.txt` files which contain only the relevant variables for our analysis. In an `Expert Mode` analysis `ALPanalysis.cpp` in `MadAnalysis5`, these files would be placed in the folder `ALPanalysis/Build/SampleAnalyzer/User/Analyzer/` and run through the command line. More information on the use of `MadAnalysis5` can be found at https://madanalysis.irmp.ucl.ac.be/. The `ALPanalysis.cpp` file produces from a `.hepmc` file of ackground events several files:
- `muon_count.txt` which contains the number of muons and antimuons in every event
- `muon_pair_count.txt` which contains the number of muon-antimuon-pairs in every event
- `muon_pair_parents.txt` which contains the PDG-ID of every muon-antimuon-pair's parent in the dataset
- `muon_data.txt` which is the data to be read into the `.ipynb` files, containing 
  - a list of all top quarks in the event (as we know there to be only one top quark in every event, this is the same top quark in different intermediate states; the last particle in the list is the 'final state' top)
  - a list of all anti-tops in the event (again, with the last in the list being the final state antitop)
  - a list of muon-antimuon-pairs (listed as muon, then antimuon)
  - a list of unpaired muons and antimuons
  - each of the particle's data is given by
    - its PDG-ID
    - its production vertex (given by the function `decay_vertex`)
    - its four-momentum (E, px, py, pz)
  - The particles' properties are separated by `\t`, the particles by `|`, and the events by `\n`.

## Running `MadAnalysis5`
- Start by running `MadAnalysis5` in expert mode `./bin/mg5 -e`. Assuming the directory and workspace is named ALPanalysis:
- Change the `ALPanalysis/Build/SampleAnalyzer/User/Analyzer/` accounding to `ALPanalysis.cpp` in the `MadAnalysis` folder
- Run `source setup.sh`
- In `ALPanalysis` compile with `make`
- Add the folder `ALPanalysis/Output/TXT` - otherwise the .txt files won't be saved while running the analysis
- Add the file `input.txt` including the path to the input background .hepmc file
- Run `./MadAnalysis5job input.txt`

## Running the .ipynb remotely with Jupyter notebook
- In lxplus start jupyter notebook with no browser `jupyter notebook --no-browser --port=<port-number>`. Specified port number is optional
- On local computer tunnel the remote local host with `ssh -N -f -L localhost:8888:localhost:<port-number> <username>@lxplus<7xx>.cern.ch`, for current lxplusnumber 7xx, and enter password
- In browser type `localhost:8888`
For VS code only first step is needed, then open browser under PORTS is VS code.
