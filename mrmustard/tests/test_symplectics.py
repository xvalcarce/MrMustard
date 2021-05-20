from thewalrus.symplectic import two_mode_squeezing, squeezing, rotation, beam_splitter, expand
import numpy as np

from mrmustard.tf import (
    Dgate,
    Sgate,
    LossChannel,
    BSgate,
    Ggate,
    Optimizer,
    Circuit,
    S2gate,
    Rgate,
    Vacuum,
)

import pytest


@pytest.mark.parametrize("r", [0.1, 1, 2])
def test_two_mode_squeezing(r):
    """Tests that the two-mode squeezing operation is implemented correctly"""
    S2 = S2gate(modes=[0, 1], r=r, phi=0.0)
    cov = S2(Vacuum(num_modes=2)).cov
    expected = two_mode_squeezing(2 * r, 0.0)
    assert np.allclose(cov, expected)


@pytest.mark.parametrize("r", np.random.rand(3))
@pytest.mark.parametrize("phi", np.random.rand(3))
def test_Sgate(r, phi):
    """Tests the Sgate is implemented correctly by applying it on one half of a maximally entangled state"""
    r_choi = np.arcsinh(1.0)
    S2 = S2gate(modes=[0, 1], r=r_choi, phi=0.0)
    S = Sgate(modes=[0], r=r, phi=phi)
    cov = S(S2(Vacuum(num_modes=2))).cov
    expected = two_mode_squeezing(2 * r_choi, 0.0)
    S_expanded = expand(squeezing(r, phi), [0], 2)
    expected = S_expanded @ expected @ S_expanded.T
    assert np.allclose(cov, expected)


@pytest.mark.parametrize("theta", [0, np.pi / 4, np.pi / 2])
def test_Rgate(theta):
    """Tests the Rgate is implemented correctly by applying it on one half of a maximally entangled state"""
    r_choi = np.arcsinh(1.0)
    S2 = S2gate(modes=[0, 1], r=r_choi, phi=0.0)
    R = Rgate(modes=[0], angle=theta)
    cov = R(S2(Vacuum(num_modes=2))).cov
    expected = two_mode_squeezing(2 * r_choi, 0.0)
    S_expanded = expand(rotation(theta), [0], 2)
    expected = S_expanded @ expected @ S_expanded.T
    assert np.allclose(cov, expected)


@pytest.mark.parametrize("theta", np.random.rand(3))
@pytest.mark.parametrize("phi", np.random.rand(3))
def test_BSgate(theta, phi):
    """Tests the BSgate is implemented correctly by applying it on one half of a maximally entangled state"""
    r_choi = np.arcsinh(1.0)
    S2a = S2gate(modes=[0, 2], r=r_choi, phi=0.0)
    S2b = S2gate(modes=[1, 3], r=r_choi, phi=0.0)
    BS = BSgate(modes=[0, 1], theta=theta, phi=phi)
    cov = BS(S2b(S2a(Vacuum(num_modes=4)))).cov
    expected = expand(two_mode_squeezing(2 * r_choi, 0.0), [0, 2], 4) @ expand(
        two_mode_squeezing(2 * r_choi, 0.0), [1, 3], 4
    )
    S_expanded = expand(beam_splitter(theta, phi), [0, 1], 4)
    expected = S_expanded @ expected @ S_expanded.T
    assert np.allclose(cov, expected)


@pytest.mark.parametrize("r", np.random.rand(3))
@pytest.mark.parametrize("phi", np.random.rand(3))
def test_S2gate(r, phi):
    """Tests the S2gate is implemented correctly by applying it on one half of a maximally entangled state"""
    r_choi = np.arcsinh(1.0)
    S2a = S2gate(modes=[0, 2], r=r_choi, phi=0.0)
    S2b = S2gate(modes=[1, 3], r=r_choi, phi=0.0)
    S2c = S2gate(modes=[0, 1], r=r, phi=phi)
    cov = S2c(S2b(S2a(Vacuum(num_modes=4)))).cov
    expected = expand(two_mode_squeezing(2 * r_choi, 0.0), [0, 2], 4) @ expand(
        two_mode_squeezing(2 * r_choi, 0.0), [1, 3], 4
    )
    S_expanded = expand(two_mode_squeezing(r, phi), [0, 1], 4)
    expected = S_expanded @ expected @ S_expanded.T
    assert np.allclose(cov, expected)
