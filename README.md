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
- **assignment_report_track1.ipynb** : The main report containing all the results and discussion
- **core/**
    - **dyna_main.py** : The base file containing all the functions necessary for the assignment.
    - **mazes.py** : An interface for the pycolab game engine.
- **utils/**
    - **create_config.py** : An utility script for creating configuration files for the experiments.
- **config/**
    - **blocking.config** : An example blocking maze configuration file
    - **shortcut.config** : An example shortcut maze configuration file

### Running the notebook:
We have already run the notebook and our graphs can be viewed within it on this repository. However, the notebook needs to be run if you wish to see the animation from the last section (**Visualizing the value function**). To do so, simply clone the repository and run jupyter inside the repository:
```
jupyter notebook
```
From there, you can simply select **assignment_report_track1.ipynb** in your jupyter tab on your browser. When running the assignment report notebook, please note that the number of simulations set by default is at (n = 500). Please be patient as the algorithm takes about a minute to run in certain sections of the notebook.
