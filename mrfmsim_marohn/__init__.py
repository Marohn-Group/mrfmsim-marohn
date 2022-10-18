import os
import yaml

# load units
DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(DIR, "units.yaml"), "r") as config:
    UNITS = yaml.load(config, Loader=yaml.BaseLoader)
