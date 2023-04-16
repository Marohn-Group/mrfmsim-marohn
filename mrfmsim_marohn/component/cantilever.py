#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines cantilever objects."""

import numpy as np
from mrfmsim.component import ComponentBase
from mrfmsim_marohn import UNITS


class Cantilever(ComponentBase):
    """cantilever object."""

    _units = UNITS

    def __init__(self, k_c, f_c):
        """Initialize cantilever.
    
        :param float k: spring constant [nN/m]
        :param float f: mechanical resonance freq [mHz]
        :ivar float k: spring constant [nN/m]
        :ivar float f: mechanical resonance freq [mHz]
        """
        self.k_c = k_c
        self.f_c = f_c

    def dk_to_df_ac_cermit(self, dk_spin):
        """Converting spring constant to the frequency.

        The ac cermit uses modulation and the resulting frequency shift
        is the fourier component. The fourier component of a square
        wave modulating between 1 and 0 is 2/pi, but we are modulating betw
        
        
        The primary Fourier component of a square wave is 4/pi.
        You lose a factor of two because you modulate between 1 and 0 and
        not 1 and -1. The final factor of 1/sqrt(2) is because we report
        rms instead of peak amplitude.
        """
        return dk_spin * self.f_c / (self.k_c * np.pi * np.sqrt(2))

    def dk_to_df_dc_cermit(self, dk_spin):
        """Converting spring constant to the frequency.

        The dc cermit for the direct frequency shift.
        """
        return dk_spin * self.f_c / (2 * self.k_c)
