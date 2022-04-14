# ttalps

## Structure of the code

The code is made up of four auxiliary python files:
- The file `aux.py` contains the input and output paths used in all Jupyter notebooks as well as the HiddenPrints context manager.
- The file `data_classes.py` contains the definitions of the classes for `FourVector`, `FourMomentum`, `Particle`, `Event`, and `Dataset` which we encapsulate our data in.
- The file `myplot.py` contains convenient shortcuts to plots we use, as well as their colour scheme.
- The file `physics.py` contains the used interface to TdAlps, functions for the calculation of lifetimes and branching ratios, as well as a dictionary of the physical constants needed, `sm`.

We use these .py-files in the Jupyter notebooks:
- `Decays.ipynb` explores the ALPs lifetime and branching ratio in the considered coupling setup
- `Data_Exploration.ipynb` works with the samples to explore the generated events' parameter space
