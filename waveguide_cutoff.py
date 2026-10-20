"""Cutoff frequencies of a rectangular waveguide (illustrative helper).

Supporting calculation for the TIPE on microwave heating: a rectangular
waveguide of width a and height b only propagates a mode if the frequency is
above its cutoff frequency. Below it, the wave is evanescent.
"""
import math

C = 299_792_458.0  # speed of light in vacuum (m/s)


def cutoff_frequency(a, b, m, n, eps_r=1.0):
    """Cutoff frequency (Hz) of the TE/TM(m, n) mode of a rectangular waveguide.

    a, b  : inner dimensions in metres (a is the wider side)
    m, n  : mode indices
    eps_r : relative permittivity of the filling material
    """
    v = C / math.sqrt(eps_r)
    return 0.5 * v * math.sqrt((m / a) ** 2 + (n / b) ** 2)


def is_propagating(f, a, b, m, n, eps_r=1.0):
    """True if a wave of frequency f (Hz) propagates in the mode (m, n)."""
    return f > cutoff_frequency(a, b, m, n, eps_r)


if __name__ == "__main__":
    F_OVEN = 2.45e9  # domestic microwave oven frequency (Hz)
    A, B = 0.086, 0.043  # example dimensions (m), a standard WR-340 guide
    fc = cutoff_frequency(A, B, 1, 0)
    print(f"TE10 cutoff: {fc / 1e9:.3f} GHz")
    print("Propagates at 2.45 GHz:", is_propagating(F_OVEN, A, B, 1, 0))
