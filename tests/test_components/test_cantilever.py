#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrfmsim_marohn.components import Cantilever
import numpy as np
import pytest

CANT_REPR = """Cantilever(
  f_c=4.975e+06 [mHz] # cantilever mechanical resonance frequency
  k_c=7.800e+05 [nN/m] # cantilever spring constant
)"""


class TestCantilever:
    @pytest.fixture
    def cantilever(self):
        return Cantilever(k_c=7.8e5, f_c=4.975e6)

    def test_k_to_f(self, cantilever):
        """Test k_to_f conversion"""

        k = 2.0
        assert np.isclose(cantilever.k_to_f(k), 2.87120)

    def test_str(self, cantilever):
        """Test cantilever repr"""

        assert str(cantilever) == CANT_REPR
