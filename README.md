# Assignment: Planning and Temporal Abstraction

## Track 1 : Dyna-Q

**Team members:** Nikhil Kakodkar (McGill ID: 260578689) & Karim Koreitem (McGill ID: 260460964)

### Setup:
Install Pycolab:
```
pip install git+https://github.com/deepmind/pycolab.git
```
clone repo:
```
git clone https://github.com/rllabmcgill/planning-temporal-abstraction-dynaqties.git
```

### Files and Folders:
- **track1_part1_dynaQ.ipynb** : The main report containing all the results and discussion for Part 1 (DynaQ experiments) of the assignment
- **track1_part2_experience_replay.ipynb** : The main report containing all the results and discussion for Part 2 (Experience replay discussion) of the assignment
- **core/**
    - **dyna_main.py** : The base file containing all the functions necessary for the assignment.
    - **mazes.py** : An interface for the pycolab game engine.
- **utils/**
    - **create_config.py** : An utility script for creating configuration files for the experiments.
    - **utils.py** : A python library containing utility functions.
- **config/**
    - **blocking.config** : An example blocking maze configuration file
    - **shortcut.config** : An example shortcut maze configuration file

### IMPORTANT NOTE:
Github does not render the animations we have included in the last section of *track1_part1_dynaQ.ipynb* (**Visualizing the value function**), which shows the evolution of the Q-value as number of steps increases. To see this please download the notebook.
