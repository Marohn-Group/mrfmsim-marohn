"""Import the experiments dynamically to the mrfmsim_marohn.experiments module"""


import sys
import glob
import os
from mrfmsim.configuration import MrfmSimLoader
import yaml

DIR = os.path.dirname(os.path.realpath(__file__))
exp_list = glob.glob(os.path.join(DIR, '**/*.yaml'), recursive=True)

for exp_path in exp_list:

    exp_name = os.path.splitext(os.path.basename(exp_path))[0]
    module_name = f"mrfmsim_marohn.experiments.{exp_name}"
    with open(exp_path) as f:
        sys.modules[module_name] = yaml.load(f, MrfmSimLoader)
