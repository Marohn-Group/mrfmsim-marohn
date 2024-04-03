"""Import the experiments dynamically to the mrfmsim_marohn.experiment module."""


import sys
import glob
import os
from mrfmsim.configuration import MrfmSimLoader
import yaml

DIR = os.path.dirname(os.path.realpath(__file__))
exp_list = glob.glob(os.path.join(DIR, "**/*.yaml"), recursive=True)
# symbolic link to the experiment directory
# the experiments are not loaded yet
experiment_path_dict = {}
for exp_path in sorted(exp_list):
    exp_name = os.path.splitext(os.path.basename(exp_path))[0]
    experiment_path_dict[exp_name] = exp_path

current_module = sys.modules[__name__]

# dynamically load the experiment when accessed
# The design does not load all the experiments at once during testing
# helps to debug errors. Otherwise, an error in the configuration
# gives errors to all testing modules.
# The design does not affect the plugin loading, however, since all the
# attributes are accessed at the front and are therefore loaded.


def __getattr__(name: str):
    if name in current_module.__dict__:
        return getattr(current_module, name)
    elif name in experiment_path_dict:
        exp_path = experiment_path_dict[name]
        with open(exp_path) as f:
            exp = yaml.load(f, MrfmSimLoader)
            setattr(current_module, name, exp)
            return exp
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")


def show():
    """Show the list of experiments."""
    print("The list of available collections/experiments:")
    for exp_name in experiment_path_dict:
        print(f"{exp_name}")


__mrfmsim_plugin__ = list(experiment_path_dict.keys())
