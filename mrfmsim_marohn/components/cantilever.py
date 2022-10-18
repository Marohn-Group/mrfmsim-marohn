#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines cantilever objects"""

from re import U
import numpy as np
from mrfmsim.component import ComponentBase
from mrfmsim_marohn import UNITS

class Cantilever(ComponentBase):

    """cantilever object"""

    _units = UNITS

    def __init__(self, k_c, f_c):
        """Initialize cantilever
        :param float k: spring constant [nN/m]
        :param float f: mechanical resonance freq [mHz]
        :ivar float k: spring constant [nN/m]
        :ivar float f: mechanical resonance freq [mHz]
        """
        self.k_c = k_c
        self.f_c = f_c

    def k_to_f(self, k):
        """Coefficient for converting spring constant to frequency
    
        :param float/np.array force gradient signal
        :return float/np.array frequency signal
        """
        return k * self.f_c / (self.k_c * np.pi * np.sqrt(2))
