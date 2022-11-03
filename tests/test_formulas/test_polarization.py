"""Test teh relative change in polarization"""

import mrfmsim_marohn.formulas.polarization as pol
import numpy as np
from mrfmsim_marohn.components import Sample
import pytest


@pytest.fixture
def sample_e():
    """Electron sample"""
    return Sample(spin_type="electron", temperature=0.001, T1=1.0, T2=1.0, spin_density=10.0)


@pytest.fixture
def sample_h():
    """Nucleus sample"""
    return Sample(spin_type="1H", temperature=4.2, T1=10, T2=5e-6, spin_density=49.0)


def test_rel_dpol_sat(sample_e):
    """Test the *absolute* tolerance

    Sample -> e -> electron spin, J = 1/2, high field limit
    """

    p1 = pol.rel_dpol_sat(0.0, 0.0, sample_e.dB_sat, sample_e.dB_hom)
    # depolarized
    p2 = pol.rel_dpol_sat(0.0, 1.0, sample_e.dB_sat, sample_e.dB_hom)
    # polarized
    p3 = pol.rel_dpol_sat(100.0, 1.0e-3, sample_e.dB_sat, sample_e.dB_hom)

    assert np.allclose([0.0, -1.0, 0.0], [p1, p2, p3])


def test_rel_dpol_arp_ibm(sample_h):
    """Test rpol_arp_ibm

    Sample -> proton spin -> rpol_arp_ibm() limiting cases
    Sample -> h -> proton spin
    """

    # on resonance
    n1 = pol.rel_dpol_arp_ibm(0.0, 2.0e6, sample_h.Gamma)
    # below resonance
    n2 = pol.rel_dpol_arp_ibm(-100.0, 2.0e6, sample_h.Gamma)
    # above resonance
    n3 = pol.rel_dpol_arp_ibm(100.0, 2.0e6, sample_h.Gamma)

    assert np.allclose([n1, n2, n3], [-1.0, 0.0, 0.0])


def test_rel_dpol_nut(sample_h):
    """Test rel_dpol_nut
    Sample -> proton spin -> rpol_nut(), on resonance pulses
    Sample -> h -> proton spin
    """

    Gamma = 0.0425774805964  # gyromagnetic ratio in MHz/mT
    rabi = 1.0 / (Gamma)  # Rabi period in microseconds for 1 mT

    # pi/2 pulse
    rpol_090 = pol.rel_dpol_nut(0.0, 1.0, sample_h.Gamma, 0.25 * rabi * 1.0e-6)

    # pi pulse
    rpol_180 = pol.rel_dpol_nut(0.0, 1.0, sample_h.Gamma, 0.50 * rabi * 1.0e-6)

    assert np.allclose([rpol_090, rpol_180], [-1.0, -2.0])


def test_rel_dpol_arp(sample_h):
    """Test rel_dpol_arp
    if f_fm is close to infinity, the relative change in polarization
    is -2.0
    if b1 and the modulation frequency is small and b_offset is large
    the spin does not flip therefore the relative change in polarization
    is close to 0.0 (off resonance case)
    """

    rpol_180 = pol.rel_dpol_arp(0.0, 1.0, 1e10, sample_h.Gamma)
    assert np.isclose(rpol_180, -2.0)

    rpol_0 = pol.rel_dpol_arp(10000.0, 0.1, 0.1, sample_h.Gamma)

    assert np.isclose(0.0, rpol_0)


def test_rel_dpol_periodic_irrad_cont(sample_e):
    """Test rel_dpol_periodic_irrad in the continuous case
    When the if t_off is 0, the intermittent irradiation becomes continuous
    irradiation. This should be the same as rel_dpol_sat
    When t_on is 0, the signal should vanish
    """
    # continuous
    rpol_cont = pol.rel_dpol_periodic_irrad(
        0,
        1.0,
        sample_e.dB_sat,
        sample_e.dB_hom,
        sample_e.T1,
        t_on=10 * sample_e.T1,
        t_off=0,
    )
    rpol = pol.rel_dpol_sat(0, 1.0, sample_e.dB_sat, sample_e.dB_hom)

    assert np.isclose(rpol_cont, rpol)


def test_rel_dpol_periodic_irrad_no_irrad(sample_e):
    """Test rel_dpol_periodic_irrad in no irradiation case
    When t_on is 0, the signal should vanish
    """

    rpol_0 = pol.rel_dpol_periodic_irrad(
        0, 1.0, sample_e.dB_sat, sample_e.dB_hom, sample_e.T1, t_on=0, t_off=2e-4
    )

    assert np.equal(rpol_0, 0.0)


def test_rel_dpol_periodic_irrad_off_res(sample_e):
    """Test rel_dpol_periodic_irrad off resonance case
    When is it off resonance (b_offset is large), the signal is 0
    """

    # off-resonance case
    rpol_off_res = pol.rel_dpol_periodic_irrad(
        10000,
        0.5,
        sample_e.dB_sat,
        sample_e.dB_hom,
        sample_e.T1,
        t_on=4e-5,
        t_off=2e-4,
    )

    assert np.isclose(rpol_off_res, 0.0)
