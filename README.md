# ttalps

This GitLab repository contains the code so far accumulated in the exploration of signatures of ALPs produced together with a top antitop pair at the CMS detector at the LHC, with the ALP decaying into a muon pair. We use this code to compare the signatures of signal events (tta->ttmumu) with background events which do not have an ALP (ttmumu) to separate the two sets of events on the basis of their kinematic variables.

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

The folder `MadAnalysis` contains `.cpp` and `.h` files that are scripts for the program `MadAnalysis5` which is used here to convert `.hepmc` files with generated events to `.txt` files which contain only the relevant variables for our analysis. In an `Expert Mode` analysis `ALPanalysis.cpp` in `MadAnalysis5`, these files would be placed in the folder `ALPanalysis/Build/SampleAnalyzer/User/Analyzer/` and run through the command line. More information on the use of `MadAnalysis5` can be found at https://madanalysis.irmp.ucl.ac.be/.
