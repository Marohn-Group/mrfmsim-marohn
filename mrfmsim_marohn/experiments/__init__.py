"""Import the experiments dynamically to the mrfmsim_marohn.experiments module."""


import sys
import glob
import os
from mrfmsim.configuration import MrfmSimLoader
import yaml


DIR = os.path.dirname(os.path.realpath(__file__))
exp_list = glob.glob(os.path.join(DIR, "**/*.yaml"), recursive=True)

experiment_dict = {}
for exp_path in sorted(exp_list):
    exp_name = os.path.splitext(os.path.basename(exp_path))[0]

    with open(exp_path) as f:
        exp = yaml.load(f, MrfmSimLoader)
        experiment_dict[exp_name] = exp

globals().update(experiment_dict)

def show():
    """Show the list of experiments."""
    print("The list of available experiments:")
    for exp_name in experiment_dict:
        print(f"{exp_name}")
